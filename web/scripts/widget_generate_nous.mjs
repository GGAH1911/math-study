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

const EV = `${MON}/events.ndjson`;
const emit = (o) => { try { appendFileSync(EV, JSON.stringify({ t: Date.now(), ...o }) + '\n'); } catch { /* 모니터는 best-effort */ } };

// ── 프롬프트: widget_generate.mjs 와 동일해야 비교가 성립한다(수정 시 양쪽 같이) ──────────
const HEAD = `너는 한국 수학 개념을 **인터랙티브 시각화(InteractiveSpec)**로 만든다. 출력은 {"spec":..., "recipe":...} JSON 하나만(코드펜스 없이).

InteractiveSpec 형식:
{ "title", "params":[{"name","label","type":"slider","min","max","init","step","unit"}], "scope":"mathjs ;구분 대입식(슬라이더값→보조변수)", "geometry":{"range":[x0,x1],"yRange":[y0,y1],"showAxes":true,"showGrid":true,"shapes":[{"type":"circle|point|segment|line|polygon", ...좌표/값에 \\"=식\\" 가능}]}, "plot":{"range","yRange","fns":[{"fn","label","color"}]}, "readout":[{"label","expr","digits"}] }
- \\"=식\\"은 어디든 mathjs로 scope에서 평가(scope변수 사용). **함수 그래프가 핵심이면 plot만 써라** — plot이 있는데 geometry에 곡선 없이 점·선분만 찍는 건 **금지**(중복·혼란). geometry는 곡선이 없는 진짜 도형(원·다각형·단위원·벡터·각)일 때만. 슬라이더 돌리면 실시간 갱신.
예시(단위원·삼각비): {"params":[{"name":"theta","label":"θ","type":"slider","min":0,"max":360,"init":30,"step":1}],"scope":"rad=theta*pi/180; cx=cos(rad); sy=sin(rad)","geometry":{"range":[-1.4,1.4],"yRange":[-1.4,1.4],"showAxes":true,"shapes":[{"type":"circle","center":[0,0],"radius":1},{"type":"point","at":["=cx","=sy"],"label":"P"}]},"readout":[{"label":"sin","expr":"sy"}]}

recipe(검증용 — 매우 중요): {"samples":[{슬라이더값}×3~4],"invariants":["scope변수로 쓴 수학 항등식; 모든 샘플서 절댓값 ≈0이어야"],"oracle":[{"params":{슬라이더값},"expect":{"scope변수":손계산값}}×2~3],"tol":1e-6}
- invariants는 개념의 **수학적 사실에서 유도**: 단위원→"cx^2+sy^2-1", 곡선 위 점이면 그 점이 식 만족, 접선기울기=도함수 등.
- oracle의 expect는 **네가 독립적으로 손계산한 정답**(예 theta=30°면 sy=0.5).

개념의 핵심을 슬라이더로 탐구하게 하는 spec + 그 정답을 강제하는 recipe를 만들어라. 본문:
`;

function bodyOf(id) {
  for (const cand of [`${CDIR}/${id}.md`, `${CDIR}/${id.normalize('NFD')}.md`, `${CDIR}/${id.normalize('NFC')}.md`]) {
    if (existsSync(cand)) { const m = readFileSync(cand, 'utf8').match(/^---\n[\s\S]*?\n---\n([\s\S]*)$/); if (m) return m[1].replace(/\s+/g, ' ').trim().slice(0, 700); }
  }
  return '';
}

async function gen(id, idx, total) {
  const body = bodyOf(id);
  emit({ ev: 'start', id, idx, total, model: MODEL });
  if (!body) { emit({ ev: 'done', id, ok: false, why: '본문없음' }); return { id, ok: false, why: '본문없음' }; }
  const t0 = Date.now();

  let r;
  try {
    r = await fetch(`${BASE}/chat/completions`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: MODEL,
        messages: [{ role: 'user', content: `${HEAD}\n[${id}]\n${body}` }],
        response_format: { type: 'json_object' },
        max_tokens: MAX_TOKENS,
        stream: true,
        stream_options: { include_usage: true },
      }),
    });
  } catch (e) { emit({ ev: 'done', id, ok: false, why: `네트워크: ${e.message}` }); return { id, ok: false, why: `네트워크: ${e.message}` }; }
  if (!r.ok) {
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
  for await (const chunk of r.body) {
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
const ids = argv.filter((a, i) => !a.startsWith('--') && i !== pi + 1);

emit({ ev: 'run', total: ids.length, model: MODEL, maxTokens: MAX_TOKENS, par: PAR });
const t0 = Date.now();
let pass = 0, cost = 0, qi = 0;
async function worker() {
  while (qi < ids.length) {
    const i = qi++;
    const r = await gen(ids[i], i + 1, ids.length);
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
