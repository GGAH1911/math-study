#!/usr/bin/env node
// 튜터 비전 A/B — 기출 문제 이미지를 읽고 ①전사 ②풀이·정답까지 내게 해서 모델별로 비교.
//   필기(손풀이) 데이터가 아직 0건이라 그 대체 측정이다. 문제 이미지 판독은 실제 프로덕션 경로이기도 하다
//   (문제 페이지 튜터는 --add-dir 로 문제 PNG 를 직접 본다).
//
// ★두 지표를 나눠 본다:
//   - **정답 정확도**(객관): DB answer 와 정확히 일치. 읽기+추론 합산 능력.
//   - **전사 충실도**(별도 채점): 이미지를 얼마나 정확히 읽었는가. 못 푸는 킬러여도 읽기는 잴 수 있다.
//   튜터에 필요한 1차 능력은 **읽기**다 — 학생 풀이를 오독하면 지도 자체가 틀어진다.
// ★D17: LLM 은 통이미지가 아니라 tile_for_vision 타일을 본다(다운스케일로 첨자·부호가 깨짐).
//
// 사용: NOUS_API_KEY=... node web/scripts/tutor_vision_run.mjs
import { readFileSync, writeFileSync, existsSync, mkdirSync, appendFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const REPO = process.env.WT_REPO || fileURLToPath(new URL('../..', import.meta.url)).replace(/\/$/, '');
const MON = `${REPO}/.llm-monitor`;
if (!existsSync(MON)) mkdirSync(MON, { recursive: true });
const EV = `${MON}/events.ndjson`;
const emit = (o) => { try { appendFileSync(EV, JSON.stringify({ t: Date.now(), ...o }) + '\n'); } catch { /* */ } };

const KEY = process.env.NOUS_API_KEY;
if (!KEY) { console.error('NOUS_API_KEY 없음'); process.exit(1); }
const BASE = process.env.NOUS_BASE || 'https://inference-api.nousresearch.com/v1';

const CANDIDATES = [
  { key: 'haiku', model: '~anthropic/claude-haiku-latest' },
  { key: 'gemma4-31b', model: 'google/gemma-4-31b-it' },
  { key: 'llama4-scout', model: 'meta-llama/llama-4-scout' },
  { key: 'mistral-small', model: 'mistralai/mistral-small-3.2-24b-instruct' },
  { key: 'qwen3.7-flash', model: 'qwen/qwen3.7-flash' },
];

const PROMPT = `아래 이미지는 한국 수능/모의고사 기출 수학 문제다(타일 1장 이상, 위→아래 순).

두 가지를 하라.
1) **전사**: 문제를 본문 그대로 옮겨 적는다. 수식은 KaTeX 로 쓰고($...$), 첨자·지수·부호를 절대 바꾸지 마라.
   그림이 있으면 그림이 무엇을 나타내는지(도형·좌표·표시된 값·조건) 함께 서술한다. 보기 ①-⑤ 가 있으면 전부 옮긴다.
2) **풀이**: 끝까지 풀어 최종 답을 낸다. 객관식이면 번호(1-5), 주관식이면 숫자만.

출력은 JSON 하나만(코드펜스 없이):
{"transcription":"...", "solution":"핵심 풀이 단계", "answer":"최종답(숫자만)"}`;

const set = JSON.parse(readFileSync(`${MON}/vision_set.json`, 'utf8'));
const PAR = +(process.env.VIS_PAR || 3);

// vision_set.json 은 호스트 경로(/home/insung/math-study/...)로 기록되는데 컨테이너 안 레포는 /app 이다.
// 같은 바인드마운트를 가리키므로 접두사만 갈아끼우면 된다(양방향 실행 가능).
const HOST_REPO = '/home/insung/math-study';
const localize = (p) => (p.startsWith(HOST_REPO) && REPO !== HOST_REPO ? REPO + p.slice(HOST_REPO.length) : p);

function dataUrl(p) {
  const b64 = readFileSync(localize(p)).toString('base64');
  return `data:image/png;base64,${b64}`;
}

async function ask(cand, prob, idx, total) {
  const label = `${cand.key} · ${prob.id}`;
  emit({ ev: 'start', id: label, idx, total, model: cand.model });
  const t0 = Date.now();
  const content = [
    { type: 'text', text: PROMPT },
    ...prob.tiles.map((t) => ({ type: 'image_url', image_url: { url: dataUrl(t) } })),
  ];
  try {
    const r = await fetch(`${BASE}/chat/completions`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: cand.model,
        messages: [{ role: 'user', content }],
        max_tokens: 4000,
        reasoning: { enabled: false },
      }),
    });
    if (!r.ok) {
      const why = `HTTP ${r.status}: ${(await r.text()).slice(0, 140)}`;
      emit({ ev: 'done', id: label, ok: false, why });
      return { cand: cand.key, id: prob.id, gold: prob.answer, error: why };
    }
    const j = await r.json();
    const txt = j.choices?.[0]?.message?.content || '';
    const secs = +((Date.now() - t0) / 1000).toFixed(1);
    const u = j.usage || {};
    let obj = null;
    const m = txt.match(/\{[\s\S]*\}/);
    if (m) { try { obj = JSON.parse(m[0]); } catch { /* 파싱 실패 */ } }
    const ans = String(obj?.answer ?? '').replace(/[^0-9.\-]/g, '').trim();
    const correct = ans !== '' && ans === String(prob.gold ?? prob.answer).trim();
    emit({ ev: 'done', id: label, ok: correct, why: correct ? '' : `답 ${ans || '없음'} ≠ ${prob.answer}`, secs, usage: u });
    return {
      cand: cand.key, id: prob.id, tier: prob.tier, subject: prob.subject,
      gold: String(prob.answer), answer: ans, correct,
      transcription: obj?.transcription ?? '', solution: obj?.solution ?? '',
      raw: obj ? '' : txt.slice(0, 500), secs,
      inTok: u.prompt_tokens ?? 0, outTok: u.completion_tokens ?? 0, cost: u.cost ?? 0,
    };
  } catch (e) {
    emit({ ev: 'done', id: label, ok: false, why: String(e.message).slice(0, 120) });
    return { cand: cand.key, id: prob.id, gold: prob.answer, error: String(e.message) };
  }
}

const jobs = [];
for (const p of set) for (const c of CANDIDATES) jobs.push({ p, c });
emit({ ev: 'run', total: jobs.length, model: `비전 A/B · ${CANDIDATES.length}모델 × ${set.length}문항`, par: PAR });

const results = []; let qi = 0;
async function worker() {
  while (qi < jobs.length) {
    const i = qi++; const { p, c } = jobs[i];
    const r = await ask(c, p, i + 1, jobs.length);
    results.push(r);
    console.log(`[${results.length}/${jobs.length}] ${c.key.padEnd(14)} ${p.id.slice(0, 26).padEnd(27)} ${r.error ? '오류 ' + r.error.slice(0, 50) : `${r.correct ? '✓' : '✗'} 답 ${r.answer || '-'}/${r.gold}  전사 ${r.transcription.length}자  ${r.secs}s`}`);
  }
}
await Promise.all(Array.from({ length: PAR }, worker));
writeFileSync(`${MON}/vision_results.json`, JSON.stringify(results, null, 1));
emit({ ev: 'summary', pass: results.filter((r) => r.correct).length, total: jobs.length, cost: results.reduce((s, r) => s + (r.cost || 0), 0) });

console.log('\n── 정답 정확도 ──');
for (const c of CANDIDATES) {
  const rs = results.filter((r) => r.cand === c.key);
  const ok = rs.filter((r) => r.correct).length;
  const err = rs.filter((r) => r.error).length;
  const kil = rs.filter((r) => r.tier === 'killer');
  const kilOk = kil.filter((r) => r.correct).length;
  const cost = rs.reduce((s, r) => s + (r.cost || 0), 0);
  console.log(`${c.key.padEnd(14)} ${ok}/${rs.length - err} 정답${err ? ` (오류 ${err})` : ''} · 킬러 ${kilOk}/${kil.length} · 총 $${cost.toFixed(4)}`);
}
console.log(`\n→ ${MON}/vision_results.json`);
