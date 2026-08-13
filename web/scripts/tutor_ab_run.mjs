#!/usr/bin/env node
// 튜터 모델 A/B — 후보 모델들에게 **프로덕션과 동일한 시스템 프롬프트**로 실제 학생 질문을 물어
//   답변·TTFT·비용을 수집한다. 채점은 tutor_ab_judge.mjs 가 블라인드로 한다(생성/채점 분리).
//
// ★프롬프트는 반드시 chat-context.buildTutorPrompt 를 그대로 import 해서 쓴다 — 복붙하는 순간
//   측정이 프로덕션과 갈라져 결과가 무의미해진다. 그래서 ts-resolve-hook 이 필요하다.
// ★후보는 **비전 가능 모델만** 고른다. 튜터는 학생 손풀이·문제 이미지를 봐야 하므로 text-only 는
//   애초에 후보 자격이 없다(DeepSeek V4 Flash 가 여기서 탈락).
//
// 사용: NOUS_API_KEY=... node --experimental-strip-types --import ./web/scripts/ts-resolve-hook.mjs \
//         web/scripts/tutor_ab_run.mjs [--n 14]
import { readFileSync, writeFileSync, existsSync, mkdirSync, appendFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const REPO = process.env.WT_REPO || fileURLToPath(new URL('../..', import.meta.url)).replace(/\/$/, '');
const { buildTutorPrompt, searchConcepts } = await import(`${REPO}/web/src/lib/chat-context.ts`);

const MON = `${REPO}/.llm-monitor`;
if (!existsSync(MON)) mkdirSync(MON, { recursive: true });
const EV = `${MON}/events.ndjson`;
const emit = (o) => { try { appendFileSync(EV, JSON.stringify({ t: Date.now(), ...o }) + '\n'); } catch { /* best-effort */ } };

const KEY = process.env.NOUS_API_KEY;
if (!KEY) { console.error('NOUS_API_KEY 없음'); process.exit(1); }
const BASE = process.env.NOUS_BASE || 'https://inference-api.nousresearch.com/v1';

// 후보(전부 비전 가능). baseline=현행 튜터와 같은 계열(Haiku).
const CANDIDATES = [
  // ★모델 비교가 아니라 **오개념 목록 주입 효과** 측정. 같은 모델(luna)로 ON/OFF 만 다르게 한다.
  //   블라인드 심판은 둘이 같은 모델인 줄 모르고 채점하므로, 차이가 나면 그건 주입 효과다.
  { key: 'luna-오개념OFF', model: 'openai/gpt-5.6-luna', misconceptions: false, baseline: true },
  { key: 'luna-오개념ON', model: 'openai/gpt-5.6-luna', misconceptions: true },
];

const A = process.argv.slice(2);
const N = +(A[A.indexOf('--n') + 1] || 14);
const PAR = +(process.env.AB_PAR || 4);
const cases = JSON.parse(readFileSync(`${MON}/eval_set.json`, 'utf8')).slice(0, N);

// 프로덕션 chat.ts 와 같은 순서로 대화를 조립한다(형식이 다르면 모델이 다른 걸 본다).
function buildUserPrompt(c) {
  const hist = c.history.length
    ? ['--- 이전 대화 ---', ...c.history.map((m) => `[${m.role === 'user' ? '학생' : '튜터'}]: ${m.content}`), '', '--- 학생의 새 질문 ---'].join('\n')
    : '';
  let dyn = '';
  if (c.collection === 'concepts') {
    const hits = searchConcepts(c.q, 6) || [];
    if (hits.length) {
      dyn += `\n\n--- 질문 관련 개념 후보 (개념지도에 *실존* · 링크 URL 그대로 복사) ---\n`
        + hits.map((h) => `  - ${(h.slug.split('/').pop() ?? h.slug).replace(/_/g, ' ')}${h.grade ? ` (${h.grade})` : ''}:  /concepts/${h.slug}`).join('\n');
    }
  }
  return `${dyn ? dyn + '\n\n' : ''}--- 학생과의 대화 ---\n${(hist + '\n' + c.q).trim()}`;
}

async function ask(cand, c, idx) {
  const { systemPrompt } = buildTutorPrompt(c.slug, c.collection === 'dashboard' ? 'concepts' : c.collection, undefined, { misconceptions: cand.misconceptions !== false });
  const userPrompt = buildUserPrompt(c);
  const label = `${cand.key} · ${c.slug.split('/').pop()}`;
  emit({ ev: 'start', id: label, idx, total: cases.length * CANDIDATES.length, model: cand.model });
  const t0 = Date.now();
  let ttft = null, out = '', usage = {};
  try {
    const r = await fetch(`${BASE}/chat/completions`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: cand.model,
        messages: [{ role: 'system', content: systemPrompt }, { role: 'user', content: userPrompt }],
        max_tokens: 3000, stream: true, stream_options: { include_usage: true },
        // 추론형 모델이 예산을 추론으로 다 태워 답이 0자가 되는 사고 방지(qwen3.7-flash 실측).
        // 단, 추론을 끌 수 없는 모델(gpt-5-nano)은 이 필드를 보내면 400 이라 생략한다.
        ...(cand.noReasoning === false ? {} : { reasoning: { enabled: false } }),
      }),
    });
    if (!r.ok) {
      const why = `HTTP ${r.status}: ${(await r.text()).slice(0, 160)}`;
      emit({ ev: 'done', id: label, ok: false, why });
      return { cand: cand.key, slug: c.slug, q: c.q, answer: '', error: why };
    }
    let buf = ''; const dec = new TextDecoder();
    for await (const ch of r.body) {
      buf += dec.decode(ch, { stream: true });
      let nl;
      while ((nl = buf.indexOf('\n')) !== -1) {
        const l = buf.slice(0, nl).trim(); buf = buf.slice(nl + 1);
        if (!l.startsWith('data:')) continue;
        const p = l.slice(5).trim(); if (!p || p === '[DONE]') continue;
        let j; try { j = JSON.parse(p); } catch { continue; }
        if (j.usage) usage = j.usage;
        const d = j.choices?.[0]?.delta || {};
        if (d.content) { if (ttft === null) { ttft = Date.now() - t0; emit({ ev: 'beat', id: label, idle: 0, el: Math.round(ttft / 1000) }); } out += d.content; emit({ ev: 'content', id: label, d: d.content }); }
      }
    }
  } catch (e) {
    emit({ ev: 'done', id: label, ok: false, why: String(e.message).slice(0, 120) });
    return { cand: cand.key, slug: c.slug, q: c.q, answer: '', error: String(e.message) };
  }
  const secs = +((Date.now() - t0) / 1000).toFixed(1);
  emit({ ev: 'done', id: label, ok: out.length > 0, why: out.length ? '' : '빈 응답', secs, usage });
  return {
    cand: cand.key, model: cand.model, slug: c.slug, collection: c.collection, q: c.q,
    answer: out, ttftMs: ttft, totalS: secs,
    inTok: usage.prompt_tokens ?? 0, outTok: usage.completion_tokens ?? 0, cost: usage.cost ?? 0,
  };
}

const jobs = [];
for (const c of cases) for (const cand of CANDIDATES) jobs.push({ c, cand });
emit({ ev: 'run', total: jobs.length, model: `튜터 A/B · ${CANDIDATES.length}모델 × ${cases.length}문항`, par: PAR });

const results = []; let qi = 0;
async function worker() {
  while (qi < jobs.length) {
    const i = qi++; const { c, cand } = jobs[i];
    const r = await ask(cand, c, i + 1);
    results.push(r);
    console.log(`[${results.length}/${jobs.length}] ${cand.key.padEnd(14)} ${(c.slug.split('/').pop() ?? '').slice(0, 18).padEnd(19)} ${r.error ? '오류 ' + r.error.slice(0, 60) : `${r.answer.length}자 TTFT ${r.ttftMs ?? '-'}ms $${(r.cost ?? 0).toFixed(5)}`}`);
  }
}
await Promise.all(Array.from({ length: PAR }, worker));
writeFileSync(`${MON}/ab_results.json`, JSON.stringify(results, null, 1));
emit({ ev: 'summary', pass: results.filter((r) => r.answer).length, total: jobs.length, cost: results.reduce((s, r) => s + (r.cost || 0), 0) });

console.log('\n── 모델별 요약 ──');
for (const cand of CANDIDATES) {
  const rs = results.filter((r) => r.cand === cand.key);
  const okr = rs.filter((r) => r.answer);
  const avg = (f) => okr.length ? (okr.reduce((s, r) => s + (f(r) || 0), 0) / okr.length) : 0;
  console.log(`${cand.key.padEnd(14)} 응답 ${okr.length}/${rs.length} · TTFT ${Math.round(avg((r) => r.ttftMs))}ms · 평균 ${Math.round(avg((r) => r.answer.length))}자 · 총 $${rs.reduce((s, r) => s + (r.cost || 0), 0).toFixed(4)}`);
}
console.log(`\n→ ${MON}/ab_results.json (채점: tutor_ab_judge.mjs)`);
