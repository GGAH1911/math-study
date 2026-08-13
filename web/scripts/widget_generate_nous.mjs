#!/usr/bin/env node
// 개념 → InteractiveSpec + 검증 recipe 생성기 (Nous Portal, OpenAI 호환, 스트리밍).
//   widget_generate.mjs(Opus claude -p) 의 대체 후보. 프롬프트·출력형식·검증기는 그대로 재사용한다.
//   ★진행상황을 .llm-monitor/events.ndjson 에 실시간 append → llm_monitor_server.mjs 가 SSE 로 중계.
// 사용: NOUS_API_KEY=... node web/scripts/widget_generate_nous.mjs <conceptId> [...]
//   env: NOUS_MODEL(기본 ~deepseek/deepseek-v4-flash-latest) · WT_REPO · NOUS_MAX_TOKENS
import { readFileSync, writeFileSync, existsSync, mkdirSync, appendFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const REPO = process.env.WT_REPO || fileURLToPath(new URL('../..', import.meta.url)).replace(/\/$/, '');
const { validate } = await import(`${REPO}/web/scripts/widget_validate.mjs`);
const CDIR = `${REPO}/docs/concepts`;
const OUT = process.env.NOUS_OUT || '/tmp/widget_specs';
const MON = `${REPO}/.llm-monitor`;
for (const d of [OUT, MON]) if (!existsSync(d)) mkdirSync(d, { recursive: true });

const KEY = process.env.NOUS_API_KEY || '';
if (!KEY) { console.error('NOUS_API_KEY 없음'); process.exit(1); }
const MODEL = process.env.NOUS_MODEL || '~deepseek/deepseek-v4-flash-latest';
const BASE = process.env.NOUS_BASE || 'https://inference-api.nousresearch.com/v1';
// ★reasoning 토큰이 completion 예산을 같이 먹는다(이 모델은 default_effort=high, 끌 수 없음).
//   4000 으로 잡았더니 추론만 하다 JSON 이 절단돼 4/4 전멸했다. 넉넉히 준다 — 출력 $0.224/1M 이라 싸다.
const MAX_TOKENS = +(process.env.NOUS_MAX_TOKENS || 30000);
// stuck 가드: 유휴(델타 끊김) 60s → 중단, 총 소요 300s → 중단. 실측 정상범위는 40-155s 이므로
// 여유가 충분하고, 죽은 슬롯을 10분(워커풀 spawn 타임아웃)씩 붙잡지 않는다.
const IDLE_MS = +(process.env.NOUS_IDLE_MS || 60000);
const DEADLINE_MS = +(process.env.NOUS_DEADLINE_MS || 300000);

const EV = `${MON}/events.ndjson`;
// ★워커풀에서 자식 여러 개가 같은 파일에 append 한다. O_APPEND 는 PIPE_BUF(4096) 이하 쓰기만
//   원자적이라, 그보다 큰 델타는 줄이 섞여 JSON 이 깨진다 → 1200자 단위로 쪼개 emit.
const emit = (o) => {
  try {
    if (typeof o.d === 'string' && o.d.length > 1200) {
      for (let i = 0; i < o.d.length; i += 1200) emit({ ...o, d: o.d.slice(i, i + 1200) });
      return;
    }
    appendFileSync(EV, JSON.stringify({ t: Date.now(), ...o }) + '\n');
  } catch { /* 모니터는 best-effort */ }
};

// ── 프롬프트: widget_generate.mjs 와 동일해야 비교가 성립한다(수정 시 양쪽 같이) ──────────
const HEAD = `**Reasoning language: English ONLY.** Every word of your internal reasoning must be in English — never Chinese, never Korean, not even for quoted terms (translate them to English instead). Only the user-facing strings in the final JSON (title, label, readout label) are written in Korean.

너는 한국 수학 개념을 **인터랙티브 시각화(InteractiveSpec)**로 만든다. 출력은 {"spec":..., "recipe":...} JSON 하나만(코드펜스 없이).

InteractiveSpec 형식:
{ "title", "params":[{"name","label","type":"slider","min","max","init","step","unit"}], "scope":"mathjs ;구분 대입식(슬라이더값→보조변수)", "geometry":{"range":[x0,x1],"yRange":[y0,y1],"showAxes":true,"showGrid":true,"shapes":[{"type":"circle|point|segment|line|polygon", ...좌표/값에 \\"=식\\" 가능}]}, "plot":{"range","yRange","fns":[{"fn","label","color"}]}, "readout":[{"label","expr","digits"}] }
- \\"=식\\"은 어디든 mathjs로 scope에서 평가(scope변수 사용). **함수 그래프가 핵심이면 plot만 써라** — plot이 있는데 geometry에 곡선 없이 점·선분만 찍는 건 **금지**(중복·혼란). geometry는 곡선이 없는 진짜 도형(원·다각형·단위원·벡터·각)일 때만. 슬라이더 돌리면 실시간 갱신.
예시(단위원·삼각비): {"params":[{"name":"theta","label":"θ","type":"slider","min":0,"max":360,"init":30,"step":1}],"scope":"rad=theta*pi/180; cx=cos(rad); sy=sin(rad)","geometry":{"range":[-1.4,1.4],"yRange":[-1.4,1.4],"showAxes":true,"shapes":[{"type":"circle","center":[0,0],"radius":1},{"type":"point","at":["=cx","=sy"],"label":"P"}]},"readout":[{"label":"sin","expr":"sy"}]}

recipe(검증용 — 매우 중요): {"samples":[{슬라이더값}×3~4],"invariants":["scope변수로 쓴 수학 항등식; 모든 샘플서 절댓값 ≈0이어야"],"oracle":[{"params":{슬라이더값},"expect":{"scope변수":손계산값}}×2~3],"tol":1e-6}
- invariants는 개념의 **수학적 사실에서 유도**: 단위원→"cx^2+sy^2-1", 곡선 위 점이면 그 점이 식 만족, 접선기울기=도함수 등.
- ★invariants 는 **0에 수렴하는 수치식**이어야 한다. 비교·부등식·불리언 금지 —
  "abs(dfc) < 1e-9" 처럼 쓰면 결과가 true(=1)로 평가돼 |1| > tol 로 **무조건 실패**한다.
  "A와 B가 같다"를 검증하려면 "A - B" 라고 써라(차이가 0에 수렴).
- ★readout 의 expr 은 **수치를 내는 식**이어야 한다. 문자열·판정결과("약수"/"참") 금지 —
  검증기가 Number.isFinite 로 거른다. 참/거짓을 보여주고 싶으면 "mod(b,a)" 처럼 **수치로** 표현하라.
- oracle의 expect는 **네가 독립적으로 손계산한 정답**(예 theta=30°면 sy=0.5).
- expect는 tol=1e-6 으로 대조한다. 어림값 금지 — 소수 8자리 이상 정확히 쓰거나, **정수·유리수로 딱 떨어지는 파라미터를 골라라**.

**mathjs 문법(scope·readout·invariants·"=식" 전부 해당). 벗어나면 검증기가 즉시 reject 한다:**
- 조건분기는 삼항연산자 "조건 ? a : b" 만. **if(...) 함수는 없다.**
- 논리연산은 and · or · not (**&& || ! 는 파싱 실패한다**). 비교는 == != < <= > >=.
- 화살표함수("x -> ...")·JS 문법 없음. map/filter 콜백도 쓰지 마라. 합은 닫힌 식이나 sum([a,b,c]) 로.
- 조합·순열은 combinations(n,r) · permutations(n,r) · factorial(n). **comb·nCr·C(n,r) 은 없다.**
- 쓸 수 있는 것: ^(거듭제곱) mod(a,b) sqrt abs exp log(x)=자연로그 log(x,b) log10 round(x,n) floor ceil max min sum mean sign
- 상수는 pi · e. 삼각함수는 **라디안**(sin cos tan asin acos atan atan2) — 도수는 deg*pi/180 으로 직접 변환.
- 변수명은 영문·숫자·밑줄만(한글 변수 금지). scope 문장 구분자는 ; 이다.

개념의 핵심을 슬라이더로 탐구하게 하는 spec + 그 정답을 강제하는 recipe를 만들어라. 본문:
`;

function bodyOf(id) {
  for (const cand of [`${CDIR}/${id}.md`, `${CDIR}/${id.normalize('NFD')}.md`, `${CDIR}/${id.normalize('NFC')}.md`]) {
    if (existsSync(cand)) { const m = readFileSync(cand, 'utf8').match(/^---\n[\s\S]*?\n---\n([\s\S]*)$/); if (m) return m[1].replace(/\s+/g, ' ').trim().slice(0, 700); }
  }
  return '';
}

// ★재시도는 반드시 이전 실패를 먹여야 한다(repair). 실패의 대부분이 창의성 문제가 아니라
//   기계적 오류(mathjs API 오인·오라클 정밀도)라, 검증기가 뽑아준 fails 를 그대로 되먹이면
//   같은 주사위를 다시 굴리는 대신 그 지점만 고쳐 온다. 없이 재시도하면 같은 실패를 반복한다.
//   힌트는 워커풀(widget_spec_loop.buildHint)이 이미 정제해서 준다 — 오라클 계산값은 가려져 있고
//   (모델이 정답을 베껴 통과시키는 걸 막기 위함), 어느 검사가 통과했는지도 함께 온다. 그대로 싣는다.
const repairNote = (prev) => prev ? `\n\n**직전 시도는 검증에 실패했다. 아래를 고쳐서 다시 만들어라(같은 실수 반복 금지):**\n${prev}\n` : '';

async function gen(id, idx, total, prevFail) {
  const body = bodyOf(id);
  emit({ ev: 'start', id, idx, total, model: MODEL, retry: prevFail ? 1 : 0 });
  if (!body) { emit({ ev: 'done', id, ok: false, why: '본문없음' }); return { id, ok: false, why: '본문없음' }; }
  const t0 = Date.now();

  // ★stuck 대책. 이 모델은 출력의 85-90%가 추론 토큰이라 정상도 2-3분 걸린다 → "총 시간"만으로는
  //   느린 것과 멈춘 것을 구분 못 한다. 그래서 **유휴(마지막 델타 이후 경과)** 를 1차 기준으로 삼고,
  //   총 데드라인은 슬롯 회수용 상한으로만 둔다. 없으면 fetch 가 무한 대기해 워커 슬롯이 죽는다.
  const ac = new AbortController();
  let lastDelta = Date.now(), aborted = '';
  const idleT = setInterval(() => {
    const idle = Date.now() - lastDelta;
    if (idle > IDLE_MS) { aborted = `유휴 ${Math.round(idle / 1000)}s (델타 끊김)`; ac.abort(); }
    else if (Date.now() - t0 > DEADLINE_MS) { aborted = `데드라인 ${Math.round(DEADLINE_MS / 1000)}s 초과`; ac.abort(); }
    else emit({ ev: 'beat', id, idle: Math.round(idle / 1000), el: Math.round((Date.now() - t0) / 1000) });
  }, 5000);
  const stop = () => clearInterval(idleT);

  let r;
  try {
    r = await fetch(`${BASE}/chat/completions`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: MODEL,
        messages: [{ role: 'user', content: `${HEAD}\n[${id}]\n${body}${repairNote(prevFail)}` }],
        response_format: { type: 'json_object' },
        max_tokens: MAX_TOKENS,
        stream: true,
        stream_options: { include_usage: true },
      }),
      signal: ac.signal,
    });
  } catch (e) {
    stop();
    const why = aborted || `네트워크: ${e.message}`;
    emit({ ev: 'done', id, ok: false, why }); return { id, ok: false, why };
  }
  if (!r.ok) {
    stop();
    const why = `HTTP ${r.status}: ${(await r.text()).slice(0, 200)}`;
    emit({ ev: 'done', id, ok: false, why }); return { id, ok: false, why };
  }

  // ── SSE 스트림 파싱: reasoning/content 델타를 모아 250ms 마다 모니터로 흘린다 ──────────
  let content = '', reasoning = '', usage = {}, buf = '';
  let pendR = '', pendC = '', lastFlush = 0;
  const flush = (force) => {
    const now = Date.now();
    if (!force && now - lastFlush < 250) return;
    if (pendR) { emit({ ev: 'reason', id, d: pendR }); pendR = ''; }
    if (pendC) { emit({ ev: 'content', id, d: pendC }); pendC = ''; }
    lastFlush = now;
  };
  const dec = new TextDecoder();
  try {
    for await (const chunk of r.body) {
      lastDelta = Date.now();   // ★유휴 판정 기준점 — 청크가 오는 한 살아있는 것
      buf += dec.decode(chunk, { stream: true });
      const lines = buf.split('\n'); buf = lines.pop();
      for (const ln of lines) {
        if (!ln.startsWith('data:')) continue;
        const p = ln.slice(5).trim();
        if (!p || p === '[DONE]') continue;
        let j; try { j = JSON.parse(p); } catch { continue; }
        if (j.usage) usage = j.usage;
        const d = j.choices?.[0]?.delta || {};
        if (d.reasoning) { reasoning += d.reasoning; pendR += d.reasoning; }
        if (d.content) { content += d.content; pendC += d.content; }
      }
      flush(false);
    }
  } catch (e) {
    // abort 로 끊긴 경우 aborted 에 사유가 들어있다. 그 외는 진짜 스트림 오류.
    stop(); flush(true);
    const why = aborted || `스트림 중단: ${e.message}`;
    const secs0 = +((Date.now() - t0) / 1000).toFixed(1);
    emit({ ev: 'done', id, ok: false, why, secs: secs0, usage });
    return { id, ok: false, why, secs: secs0, usage };
  }
  stop();
  flush(true);
  const secs = +((Date.now() - t0) / 1000).toFixed(1);

  const fail = (why) => { emit({ ev: 'done', id, ok: false, why, secs, usage }); return { id, ok: false, why, secs, usage }; };
  const m = content.match(/\{[\s\S]*\}/);
  if (!m) return fail(`JSON 추출 실패(content ${content.length}자, reasoning ${reasoning.length}자 — 예산 절단 의심)`);
  let obj; try { obj = JSON.parse(m[0]); } catch (e) { return fail(`파싱: ${e.message}`); }
  if (!obj.spec || !obj.recipe) return fail('spec/recipe 누락');

  writeFileSync(`${OUT}/${id.replace(/\//g, '__')}.json`, JSON.stringify({ id, ...obj }, null, 1));
  // ★판정은 기존 수학게이트가 한다(이중유도 invariants + oracle 손계산 대조). 모델만 바뀌고 기준은 동일.
  let v; try { v = validate(obj.spec, obj.recipe); } catch (e) { return fail(`검증기 예외: ${e.message}`); }
  const why = v.ok ? '' : (v.fails || []).slice(0, 3).join(' | ');
  emit({ ev: 'done', id, ok: v.ok, why, secs, usage, spec: obj.spec });
  return { id, ok: v.ok, why, secs, usage };
}

// ── 워커풀: 건당 70-120초(추론 토큰이 대부분)라 직렬은 낭비. 순수 HTTP 라 `claude -p` 프로세스
//    스폰과 달리 동시성 비용이 없다. 429 가 보이면 --par 를 낮출 것.
const argv = process.argv.slice(2);
const pi = argv.indexOf('--par');
const PAR = pi >= 0 ? Math.max(1, +argv[pi + 1] || 1) : +(process.env.NOUS_PAR || 4);
const fi = argv.indexOf('--prev-fail');
const PREV_FAIL = fi >= 0 ? (argv[fi + 1] || '') : '';
// ★플래그 값 인덱스는 전부 제외해야 한다. pi<0 가드 없이 pi+1 을 쓰면 -1+1=0 이라
//   **첫 번째 id 를 잘라먹는다**(워커풀은 id 하나만 넘기므로 전건 즉시 실패했던 버그).
const skipIdx = new Set([pi >= 0 ? pi + 1 : -99, fi >= 0 ? fi + 1 : -99]);
const ids = argv.filter((a, i) => !a.startsWith('--') && !skipIdx.has(i));

// ★'run' 은 대시보드를 리셋한다. 워커풀(widget_spec_loop)이 건별로 이 스크립트를 1건씩 호출할 땐
//   매번 리셋되면 화면이 못 쌓이므로, 자체 배치(2건 이상)일 때만 보낸다.
if (ids.length > 1) emit({ ev: 'run', total: ids.length, model: MODEL, maxTokens: MAX_TOKENS, par: PAR });
const t0 = Date.now();
let pass = 0, cost = 0, qi = 0;
async function worker() {
  while (qi < ids.length) {
    const i = qi++;
    const r = await gen(ids[i], i + 1, ids.length, PREV_FAIL);
    if (r.ok) pass++;
    cost += r.usage?.cost || 0;
    const u = r.usage || {};
    console.log(`${r.ok ? '✓ PASS' : '✗ FAIL'} ${r.id} (${r.secs ?? '-'}s, in ${u.prompt_tokens ?? '?'}/out ${u.completion_tokens ?? '?'}, $${(u.cost ?? 0).toFixed(5)})${r.why ? '\n    ↳ ' + r.why.slice(0, 200) : ''}`);
  }
}
await Promise.all(Array.from({ length: Math.min(PAR, ids.length) }, worker));
const wall = ((Date.now() - t0) / 1000).toFixed(0);
emit({ ev: 'summary', pass, total: ids.length, cost, wall, par: PAR });
console.log(`\n합격 ${pass}/${ids.length} · ${MODEL} · par ${PAR} · 실과금 $${cost.toFixed(5)} · 벽시계 ${wall}s · 영속 ${OUT}`);
