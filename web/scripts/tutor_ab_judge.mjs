#!/usr/bin/env node
// 튜터 A/B 블라인드 채점 — ab_results.json 의 답변들을 **모델명 숨기고** 문항별로 한 번에 채점.
//   심판=포털 강모델 2명(서로 다른 계열). 문항당 심판별 1콜(후보 전부 동시 제시) → 위치 편향은 **문항마다 라벨 셔플**로 상쇄.
//   pairwise 를 N번 도는 것보다 콜 수가 적고, 같은 문맥에서 상대비교라 점수 해상도가 높다.
// 사용: node web/scripts/tutor_ab_judge.mjs
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const REPO = process.env.WT_REPO || fileURLToPath(new URL('../..', import.meta.url)).replace(/\/$/, '');
const MON = `${REPO}/.llm-monitor`;
const results = JSON.parse(readFileSync(`${MON}/ab_results.json`, 'utf8'));
// ★심판은 **구독(claude -p)** 으로 돈다. 포털(유료 API)은 제품용이고 측정·개발에 쓰지 않는다.
//   opus-5-fast 를 포털 심판으로 쓰다 심판값이 $1.78 나온 전례가 있다(측정 대상 전부보다 3배).
//   구독 인증은 CLAUDE_CODE_OAUTH_TOKEN(1년 장기 토큰) — .credentials.json 은 조용히 만료된다.
const JUDGES = (process.env.JUDGES || 'opus,sonnet').split(',');
const CLEAN = '/tmp/claude_p_clean';
try { mkdirSync(CLEAN, { recursive: true }); } catch { /* 이미 있음 */ }

// 결정적 셔플(seed=문항 인덱스) — 재현 가능하되 문항마다 라벨 위치가 달라진다.
function shuffled(arr, seed) {
  const a = [...arr];
  let s = seed * 9301 + 49297;
  for (let i = a.length - 1; i > 0; i--) {
    s = (s * 9301 + 49297) % 233280;
    const j = Math.floor((s / 233280) * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

const RUBRIC = `너는 한국 수능 수학 튜터 답변을 채점하는 엄격한 평가자다.
아래는 **같은 학생 질문**에 대한 여러 튜터의 답변이다. 누가 썼는지는 모른다(라벨은 무작위).

각 답변을 5개 항목으로 0-10점 채점하라:
1. correctness — 수학적 정확성. 틀린 식·잘못된 결론·근거 없는 단정이 있으면 크게 감점.
2. pedagogy — 학생 수준에 맞춘 단계적 유도. 답만 던지거나, 반대로 겉돌며 진도가 안 나가면 감점.
   학생이 "답까지 내달라"고 명시하면 끝까지 내주는 게 맞다(그때 안 내주면 감점).
3. korean_math — 한국 교육과정 용어·표기(근의 공식, 도함수, 정적분 등). 번역투·외국식 표기는 감점.
4. katex — 수식이 $...$ 로 감싸였고 KaTeX 로 렌더 가능한가. 순수 유니코드 수식 남발·깨진 LaTeX 는 감점.
5. honesty — 지어내지 않았는가. 존재하지 않는 문제·링크·정답을 만들어내면 0점에 가깝게.

그리고 전체 순위를 매겨라(1등이 가장 좋음).

출력은 JSON 하나만(코드펜스 없이):
{"scores":{"<라벨>":{"correctness":n,"pedagogy":n,"korean_math":n,"katex":n,"honesty":n,"note":"한 줄 평"}},
 "rank":["<라벨>", ...],
 "why":"1등을 그렇게 고른 이유 한두 문장"}`;

function judge(prompt, model) {
  return new Promise((res) => {
    const c = spawn('claude', ['-p', prompt, '--model', model, '--output-format', 'json', '--tools', ''], {
      stdio: ['ignore', 'pipe', 'ignore'], cwd: CLEAN, timeout: 300000,
      env: { ...process.env, CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS: '1' },
    });
    let out = '';
    c.stdout.on('data', (d) => (out += d));
    c.on('close', () => {
      let text = out;
      try { const j = JSON.parse(out); if (j.is_error) { console.error(`심판 ${model}: ${String(j.result).slice(0, 80)}`); return res(null); } text = j.result || out; } catch { /* raw */ }
      const m = text.match(/\{[\s\S]*\}/);
      if (!m) return res(null);
      try { res(JSON.parse(m[0])); } catch { res(null); }
    });
    c.on('error', () => res(null));
  });
}

// 문항별로 묶기
const byQ = new Map();
for (const r of results) {
  if (!r.answer) continue;
  const k = r.slug + '||' + r.q;
  if (!byQ.has(k)) byQ.set(k, []);
  byQ.get(k).push(r);
}

const LETTERS = 'ABCDEFGH';
const judged = [];
let qi = 0;
const items = [...byQ.entries()];
const PAR = +(process.env.JUDGE_PAR || 3);

async function worker() {
  while (qi < items.length) {
    const i = qi++;
    const [k, rs] = items[i];
    if (rs.length < 2) continue;
    const order = shuffled(rs, i + 1);
    const map = {};                              // 라벨 → 실제 모델
    const blocks = order.map((r, n) => {
      const L = LETTERS[n]; map[L] = r.cand;
      return `### 답변 ${L}\n${r.answer.slice(0, 6000)}`;
    }).join('\n\n');
    const [slug, q] = k.split('||');
    const prompt = `${RUBRIC}\n\n--- 학생 질문 (페이지: ${slug}) ---\n${q}\n\n--- 답변들 ---\n${blocks}`;
    // 심판 2명 병렬 → 각각 독립 판정으로 기록(평균은 아래 집계에서, 불일치는 그대로 남긴다).
    const verdicts = await Promise.all(JUDGES.map((jm) => judge(prompt, jm).then((v) => ({ judge: jm, v }))));
    const good = verdicts.filter((x) => x.v);
    if (!good.length) { console.log(`[${i + 1}/${items.length}] 채점 실패 ${slug.slice(0, 30)}`); continue; }
    for (const g of good) judged.push({ slug, q, map, judge: g.judge, verdict: g.v });
    const winners = good.map((g) => map[g.v.rank?.[0]] ?? '?');
    const agree = new Set(winners).size === 1;
    console.log(`[${i + 1}/${items.length}] ${slug.split('/').pop()?.slice(0, 20).padEnd(21)} 1위=${winners.join(' / ')}${agree ? ' ✓합치' : ' ⚠불일치'}`);
  }
}
await Promise.all(Array.from({ length: PAR }, worker));
writeFileSync(`${MON}/ab_judged.json`, JSON.stringify(judged, null, 1));

// ── 집계 ──
const agg = {};
const DIMS = ['correctness', 'pedagogy', 'korean_math', 'katex', 'honesty'];
for (const j of judged) {
  for (const [L, cand] of Object.entries(j.map)) {
    const s = j.verdict.scores?.[L]; if (!s) continue;
    agg[cand] ??= { n: 0, wins: 0, rankSum: 0, ...Object.fromEntries(DIMS.map((d) => [d, 0])) };
    agg[cand].n++;
    for (const d of DIMS) agg[cand][d] += Number(s[d]) || 0;
    const pos = (j.verdict.rank || []).indexOf(L);
    if (pos === 0) agg[cand].wins++;
    agg[cand].rankSum += pos >= 0 ? pos + 1 : (j.verdict.rank || []).length;
  }
}
const perf = {};
for (const r of results) {
  if (!r.answer) continue;
  perf[r.cand] ??= { n: 0, ttft: 0, cost: 0 };
  perf[r.cand].n++; perf[r.cand].ttft += r.ttftMs || 0; perf[r.cand].cost += r.cost || 0;
}

console.log('\n── 블라인드 채점 결과 (문항 ' + judged.length + '개) ──');
console.log('모델'.padEnd(15) + DIMS.map((d) => d.slice(0, 8).padStart(9)).join('') + '   평균  1위  평균순위   TTFT     비용/턴');
const rows = Object.entries(agg).map(([cand, a]) => {
  const means = DIMS.map((d) => a[d] / a.n);
  const overall = means.reduce((x, y) => x + y, 0) / DIMS.length;
  const p = perf[cand] || { n: 1, ttft: 0, cost: 0 };
  return { cand, means, overall, wins: a.wins, avgRank: a.rankSum / a.n, ttft: p.ttft / p.n, cost: p.cost / p.n };
}).sort((x, y) => y.overall - x.overall);
for (const r of rows) {
  console.log(r.cand.padEnd(15) + r.means.map((m) => m.toFixed(1).padStart(9)).join('')
    + `${r.overall.toFixed(2).padStart(7)}${String(r.wins).padStart(5)}${r.avgRank.toFixed(2).padStart(10)}`
    + `${Math.round(r.ttft).toString().padStart(8)}ms  $${r.cost.toFixed(5)}`);
}
writeFileSync(`${MON}/ab_summary.json`, JSON.stringify(rows, null, 1));
console.log(`\n→ ${MON}/ab_summary.json`);
