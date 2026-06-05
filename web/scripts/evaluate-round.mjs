#!/usr/bin/env node
/**
 * /evaluate-round — 한 회차(모의고사)를 체계적으로 평가.
 *
 * 난이도는 solution.solved_by(최초로 답 맞힌 모델 = 깨끗한 난이도 신호)로 본다.
 * generated_by(검증기까지 통과한 최종 모델)는 객관식 검증기-코딩 누명 때문에 부풀려져
 * 난이도로 쓰면 안 된다 (실측: escalation의 ~73%가 사실 Haiku-solvable). solved_by 미정인
 * 문제는 '미정'으로 표기하고 백필이 채우면 깨끗해진다.
 *
 * 산출: 터미널 요약 + 자체완결 HTML 리포트(/audits/eval-<round>.html) + JSON(LLM 총평용).
 *
 * 사용:  node web/scripts/evaluate-round.mjs 2027_6월모평
 *        node web/scripts/evaluate-round.mjs 2026_고1_6월모의고사 --no-mastery
 */
import { readFileSync, readdirSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import matter from 'gray-matter';

const __dirname = dirname(fileURLToPath(import.meta.url));
const WEB_ROOT = dirname(__dirname);
const REPO_ROOT = dirname(WEB_ROOT);

const has = (n) => process.argv.includes(`--${n}`);
const arg = (n, d) => { const i = process.argv.indexOf(`--${n}`); return i >= 0 ? process.argv[i + 1] : d; };
const round = (process.argv[2] && !process.argv[2].startsWith('--')) ? process.argv[2] : arg('round');
if (!round) { console.error('사용법: node evaluate-round.mjs <round_key>   예: 2027_6월모평 / 2026_고1_6월모의고사'); process.exit(1); }

// nested 구조: docs/problems/<year>/<round_dir>/*.md  (round_dir = key에서 'year_' 떼낸 것)
const [year, ...rest] = round.split('_');
const roundDir = rest.join('_');
const dir = join(REPO_ROOT, 'docs', 'problems', year, roundDir);
if (!existsSync(dir)) { console.error(`회차 폴더 없음: ${dir}`); process.exit(1); }
const files = readdirSync(dir).filter((f) => f.endsWith('.md'));
if (!files.length) { console.error(`md 없음: ${dir}`); process.exit(1); }

const probs = files.map((f) => {
  const { data: fm } = matter(readFileSync(join(dir, f), 'utf-8'));
  const s = fm.solution || {};
  return {
    stem: f.replace(/\.md$/, ''),
    subject: fm.source?.subject ?? '?',
    number: Number(fm.source?.number ?? 0),
    score: fm.source?.score ?? null,
    format: fm.format ?? '?',
    fig: !!fm.has_figure,
    answer: fm.answer != null ? String(fm.answer) : '',
    tier: fm.killer_tier ?? null,
    unit: fm.unit && fm.unit !== 'None' ? fm.unit : null,
    concepts: (fm.concepts || []).map((c) => String(c).replace(/^docs\/concepts\//, '').replace(/\.md$/, '')),
    intent: fm.exam_intent ?? '',
    gen: fm.solution ? (s.generated_by ?? null) : null,
    solved: s.solved_by ?? null,
    esc: Array.isArray(s.escalation) ? s.escalation : [],
    cached: !!fm.solution,
    img: fm.problem_image ?? null,
  };
}).sort((a, b) => String(a.subject).localeCompare(String(b.subject)) || a.number - b.number);

const N = probs.length;
const tally = (arr, key) => arr.reduce((m, x) => { const k = key(x); m[k] = (m[k] || 0) + 1; return m; }, {});
const fmtTally = (o, order) => (order || Object.keys(o).sort()).filter((k) => o[k]).map((k) => `${k} ${o[k]}`).join(' · ');

// ── 구성 ──
const bySubject = tally(probs, (p) => p.subject);
const byScore = tally(probs, (p) => p.score ?? '?');
const byFormat = tally(probs, (p) => p.format);
const totalScore = probs.reduce((s, p) => s + (Number(p.score) || 0), 0);
const CIRC = { 1: '①', 2: '②', 3: '③', 4: '④', 5: '⑤' };
const choiceAns = tally(probs.filter((p) => p.format === 'choice'), (p) => p.answer);
const nChoice = probs.filter((p) => p.format === 'choice').length;
const ansSkew = nChoice ? Math.max(...[1, 2, 3, 4, 5].map((k) => choiceAns[k] || 0)) - Math.min(...[1, 2, 3, 4, 5].map((k) => choiceAns[k] || 0)) : 0;

// ── 난이도 (solved_by) ──
const DIFF = { haiku: '쉬움', sonnet: '중상', opus: '킬러' };
const DIFF_ORDER = ['haiku', 'sonnet', 'opus'];
const solvedP = probs.filter((p) => p.solved);
const bySolved = tally(solvedP, (p) => p.solved);
const undet = probs.filter((p) => p.cached && !p.solved).length;       // 백필 대기
const uncached = probs.filter((p) => !p.cached).length;
const diffIdx = (m) => DIFF_ORDER.indexOf(m);
const avgDiff = solvedP.length ? solvedP.reduce((s, p) => s + diffIdx(p.solved), 0) / solvedP.length : null;

// ── 검증기 건강 (escalation) ──
const verifyFail = probs.filter((p) => p.esc.some((e) => e?.reason === 'verify-fail')).length;

// ── 주목 문제 ──
const realKillers = solvedP.filter((p) => p.solved === 'opus');
const isMismatch = (p) => p.tier && p.solved && (
  (['early', 'mid'].includes(p.tier) && p.solved === 'opus') ||   // 쉬움 라벨인데 진짜 킬러(과소라벨)
  (p.tier === 'killer' && p.solved === 'haiku'));                 // 킬러 라벨인데 Haiku-easy(과대라벨)
const mismatch = solvedP.filter(isMismatch);

// ── 커버리지 ──
const byUnit = tally(probs.filter((p) => p.unit), (p) => p.unit);
const allConcepts = [...new Set(probs.flatMap((p) => p.concepts))];

// ── mastery overlay (best-effort) ──
let weakCovered = [];
if (!has('no-mastery')) {
  const cgPath = join(WEB_ROOT, 'src', 'data', 'concept-graph.json');
  if (existsSync(cgPath)) {
    try {
      const cg = JSON.parse(readFileSync(cgPath, 'utf-8'));
      const mastery = {};
      for (const n of cg.nodes || []) { const b = String(n.slug || '').split('/').pop(); if (b) mastery[b] = n.mastery; }
      weakCovered = allConcepts.filter((c) => mastery[c] === 'learning');  // 'unknown'(미학습)은 약점 아님
    } catch { /* graceful */ }
  }
}

// ── 품질 ──
const emptyAns = probs.filter((p) => !p.answer);
const outRange = probs.filter((p) => p.format === 'choice' && !['1', '2', '3', '4', '5'].includes(p.answer));

// ════════ 터미널 요약 ════════
console.log(`\n═══ 평가: ${round} (${N}문항) ═══`);
console.log(`구성   : ${fmtTally(bySubject)} | 배점 ${fmtTally(byScore, ['2', '3', '4'])} (총 ${totalScore}점) | ${fmtTally(byFormat)}`);
console.log(`난이도 : ${DIFF_ORDER.filter((m) => bySolved[m]).map((m) => `${DIFF[m]} ${bySolved[m]}`).join(' · ') || '—'}`
  + `${undet ? ` | 미정 ${undet}(백필대기)` : ''}${uncached ? ` | 미캐시 ${uncached}` : ''}`);
console.log(`검증기 : verify-fail로 escalate ${verifyFail}건 (${N ? Math.round(100 * verifyFail / N) : 0}%)  ← 난이도 아님(파이프라인 지표)`);
console.log(`주목   : 진짜킬러(opus) ${realKillers.length ? realKillers.map((p) => p.stem.split('_').slice(-2).join('_')).join(', ') : '없음'}`);
if (mismatch.length) console.log(`         라벨불일치 ${mismatch.map((p) => `${p.stem.split('_').slice(-2).join('_')}(${p.tier}→${p.solved})`).join(', ')}`);
console.log(`커버리지: 단원 ${Object.keys(byUnit).length}개 · 개념 ${allConcepts.length}개${weakCovered.length ? ` · 내 약점개념 ${weakCovered.length}개 교차(근사)` : ''}`);
console.log(`객관답 : ${[1, 2, 3, 4, 5].map((k) => `${CIRC[k]}${choiceAns[k] || 0}`).join(' ')}${ansSkew >= 3 ? `  ⚠편중(편차${ansSkew})` : ''}`);
console.log(`품질   : 정답누락 ${emptyAns.length} · 범위초과 ${outRange.length}${emptyAns.length + outRange.length === 0 ? ' ✓' : ''}`);

// ════════ JSON (LLM 총평용) ════════
const report = {
  round, year, roundDir, total: N, generated_at_note: 'stamp after run',
  composition: { bySubject, byScore, byFormat, totalScore, choiceAns, ansSkew },
  difficulty: { bySolved, undetermined: undet, uncached, avgDiff, note: 'solved_by 기준 — generated_by는 검증기 누명으로 난이도 부정확' },
  verifier_health: { verify_fail_escalations: verifyFail },
  highlights: {
    real_killers: realKillers.map((p) => ({ stem: p.stem, subject: p.subject, number: p.number, score: p.score, tier: p.tier })),
    label_mismatch: mismatch.map((p) => ({ stem: p.stem, tier: p.tier, solved_by: p.solved })),
  },
  coverage: { units: byUnit, concepts: allConcepts.length, weak_covered: weakCovered },
  quality: { empty_answer: emptyAns.map((p) => p.stem), out_of_range: outRange.map((p) => p.stem) },
  problems: probs.map((p) => ({ stem: p.stem, subject: p.subject, number: p.number, score: p.score, format: p.format, fig: p.fig, tier: p.tier, solved_by: p.solved, generated_by: p.gen, unit: p.unit, intent: p.intent })),
};
const outDir = join(WEB_ROOT, 'public', 'audits');
mkdirSync(outDir, { recursive: true });
const jsonPath = join(outDir, `eval-${round}.json`);
writeFileSync(jsonPath, JSON.stringify(report, null, 2), 'utf-8');

// ════════ HTML 리포트 ════════
const bar = (parts) => `<div class="bar">${parts.filter((p) => p.n).map((p) => `<span style="flex:${p.n};background:${p.c}" title="${p.label} ${p.n}">${p.n}</span>`).join('')}</div>`;
const diffBar = bar([
  { n: bySolved.haiku || 0, c: '#34d399', label: '쉬움' },
  { n: bySolved.sonnet || 0, c: '#fbbf24', label: '중상' },
  { n: bySolved.opus || 0, c: '#f87171', label: '킬러' },
  { n: undet, c: '#cbd5e1', label: '미정' },
]);
const probRow = (p) => `<tr class="${p.solved === 'opus' ? 'k' : ''}"><td>${p.subject} ${p.number}</td><td>${p.score ?? ''}점</td><td>${p.format === 'choice' ? '객관' : '단답'}${p.fig ? '·도형' : ''}</td>`
  + `<td class="d-${p.solved || 'x'}">${p.solved ? DIFF[p.solved] : (p.cached ? '미정' : '미캐시')}</td>`
  + `<td>${p.tier ?? ''}${isMismatch(p) ? ' ⚠' : ''}</td>`
  + `<td>${p.unit ?? ''}</td><td class="i">${p.intent}</td></tr>`;
const html = `<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><title>평가 ${round}</title><style>
body{font:14px/1.55 system-ui,sans-serif;max-width:1180px;margin:1.5em auto;padding:0 1em;color:#1f2937}
h1{font-size:1.5em;margin:.2em 0}h2{font-size:1.05em;margin:1.4em 0 .5em;border-bottom:2px solid #eef2ff;padding-bottom:.2em}
.cards{display:flex;gap:.8em;flex-wrap:wrap;margin:.8em 0}
.card{background:#f8fafc;border:1px solid #e5e7eb;border-radius:8px;padding:.7em 1em;min-width:140px}
.card b{font-size:1.6em;display:block}.card small{color:#6b7280}
.bar{display:flex;height:26px;border-radius:5px;overflow:hidden;margin:.4em 0;font:12px/26px sans-serif;color:#fff;text-align:center}
.bar span{min-width:18px}
table{border-collapse:collapse;width:100%;font-size:13px;margin:.4em 0}
th,td{border:1px solid #e5e7eb;padding:3px 7px;text-align:left}th{background:#f1f5f9}
tr.k{background:#fef2f2}.d-haiku{color:#059669;font-weight:600}.d-sonnet{color:#b45309;font-weight:600}.d-opus{color:#dc2626;font-weight:700}.d-x{color:#94a3b8}
.i{color:#6b7280;max-width:340px;font-size:12px}.note{color:#6b7280;font-size:12px;background:#f8fafc;padding:.5em .8em;border-left:3px solid #cbd5e1;border-radius:4px}
.chip{display:inline-block;background:#eef2ff;border-radius:4px;padding:1px 7px;margin:1px;font-size:12px}
</style></head><body>
<h1>📊 ${round} 평가 <small style="font-weight:400;color:#6b7280">${N}문항</small></h1>
<div class="cards">
  <div class="card"><b>${totalScore}</b><small>총 배점</small></div>
  <div class="card"><b>${bySolved.opus || 0}</b><small>진짜 킬러(opus)</small></div>
  <div class="card"><b>${bySolved.haiku || 0}</b><small>쉬움(haiku)</small></div>
  <div class="card"><b>${Object.keys(byUnit).length}</b><small>출제 단원</small></div>
  <div class="card"><b>${verifyFail}</b><small>검증기 escalate</small></div>
</div>
<h2>난이도 (solved_by — 깨끗한 신호)</h2>
${diffBar}
<p class="note">난이도는 <b>최초로 답을 맞힌 모델</b>(solved_by) 기준. generated_by(검증기까지 통과한 최종 모델)는 객관식 검증기-코딩 누명으로 부풀려져 난이도로 안 씀. ${undet ? `<b>미정 ${undet}건</b>은 백필 진행 중.` : ''}</p>
<h2>구성</h2>
<div class="cards">
  <div class="card"><small>과목</small><br>${fmtTally(bySubject)}</div>
  <div class="card"><small>배점</small><br>${fmtTally(byScore, ['2', '3', '4'])}</div>
  <div class="card"><small>형식</small><br>${fmtTally(byFormat)}</div>
  <div class="card"><small>객관식 답 ①~⑤</small><br>${[1, 2, 3, 4, 5].map((k) => `${CIRC[k]}${choiceAns[k] || 0}`).join(' ')}${ansSkew >= 3 ? ` <span style="color:#dc2626">⚠편중</span>` : ''}</div>
</div>
${realKillers.length ? `<h2>🔥 진짜 킬러 (Haiku·Sonnet 둘 다 답 못 냄)</h2>${realKillers.map((p) => `<span class="chip">${p.subject} ${p.number} (${p.score}점${p.tier ? '·' + p.tier : ''})</span>`).join(' ')}` : ''}
${mismatch.length ? `<h2>⚠ 라벨 불일치 (killer_tier vs 실제)</h2>${mismatch.map((p) => `<span class="chip">${p.subject} ${p.number}: ${p.tier}→<b>${p.solved}</b></span>`).join(' ')}<p class="note">killer_tier(인제스트 Haiku 라벨)는 과소라벨 경향 — solved_by가 더 신뢰됨.</p>` : ''}
<h2>커버리지</h2>
<p>출제 단원 <b>${Object.keys(byUnit).length}</b>개 · 개념 <b>${allConcepts.length}</b>개</p>
${Object.entries(byUnit).sort((a, b) => b[1] - a[1]).map(([u, c]) => `<span class="chip">${u} ${c}</span>`).join(' ')}
${weakCovered.length ? `<h3 style="font-size:.95em">📌 이 회차가 건드리는 내 약점 개념 (근사, ${weakCovered.length})</h3>${weakCovered.slice(0, 40).map((c) => `<span class="chip" style="background:#fef9c3">${c}</span>`).join(' ')}` : ''}
${emptyAns.length + outRange.length ? `<h2>품질 경고</h2>${emptyAns.length ? `<p>정답 누락: ${emptyAns.map((p) => p.stem).join(', ')}</p>` : ''}${outRange.length ? `<p>객관식 범위초과: ${outRange.map((p) => p.stem).join(', ')}</p>` : ''}` : ''}
<h2>문항별</h2>
<table><tr><th>문항</th><th>배점</th><th>형식</th><th>난이도</th><th>tier라벨</th><th>단원</th><th>출제의도</th></tr>
${probs.map(probRow).join('\n')}</table>
<p class="note">생성: evaluate-round.mjs · 난이도=solved_by · JSON: eval-${round}.json (LLM 총평 입력)</p>
</body></html>`;
const htmlPath = join(outDir, `eval-${round}.html`);
writeFileSync(htmlPath, html, 'utf-8');

console.log(`\n리포트: /audits/eval-${round}.html  (JSON: /audits/eval-${round}.json)`);
console.log(`  → https://tme-laptop.tailf47aa4.ts.net:8443/audits/eval-${round}.html`);
