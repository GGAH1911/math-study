#!/usr/bin/env node
// redraw 갤러리 시드 — redraw-2d 그래프 도형을 gemma4로 측정해 /tmp/redraw_specs/<id>.json 에 채운다.
//   채점은 따로(redraw_loop / redraw_score_batch). 본문=md searchable_text(ground truth).
// 사용: node web/scripts/seed_redraw.mjs [--n 15] [--par 2]
import { spawn } from 'node:child_process';
import { readFileSync, writeFileSync, readdirSync, existsSync, appendFileSync, mkdirSync } from 'node:fs';
const REPO = '/home/insung/Projects/math-study';
const SPECS = '/tmp/redraw_specs';
const LOGDIR = '/tmp/ingest_logs';
for (const d of [SPECS, LOGDIR]) if (!existsSync(d)) mkdirSync(d, { recursive: true });
const A = process.argv.slice(2);
const getOpt = (k, d) => { const i = A.indexOf(k); return i >= 0 && A[i + 1] ? A[i + 1] : d; };
const N = parseInt(getOpt('--n', '15'), 10);
const PAR = parseInt(getOpt('--par', '2'), 10);   // gemma 최대 2병렬
const LOG = `${LOGDIR}/seed_redraw_${Math.floor(Date.now() / 1000)}.log`;
const log = (s) => { const l = `${new Date().toISOString()} ${s}`; console.log(l); appendFileSync(LOG, l + '\n'); };

function bonmun(id) {
  const m = id.match(/^(.+)_([^_]+)_(\d+)$/); if (!m) return '';
  const [, round, subj, num] = m; const base = `${REPO}/docs/problems/${round.split('_')[0]}`;
  if (!existsSync(base)) return '';
  for (const sub of readdirSync(base)) for (const nm of [`${id}.md`, `${round}_${subj}_${String(num).padStart(2, '0')}.md`]) {
    const p = `${base}/${sub}/${nm}`;
    if (existsSync(p)) { const mm = readFileSync(p, 'utf8').match(/\nsearchable_text: \|\n((?:  .*\n?)*)/); if (mm) return mm[1].split('\n').map((l) => l.replace(/^ {2}/, '')).join(' ').replace(/\{\{[^}]+\}\}/g, '').replace(/\s+/g, ' ').trim().slice(0, 520); }
  }
  return '';
}
const idx = JSON.parse(readFileSync(`${REPO}/web/src/data/figure-triage.json`, 'utf8'));
const have = new Set(readdirSync(SPECS).map((f) => f.replace('.json', '')));
const cands = Object.entries(idx.figures)
  .filter(([, v]) => v.suggested === 'redraw-2d' && /graph/.test(v.suggest_reason || ''))
  .map(([k, v]) => ({ id: v.problem_slug, img: k }))
  .filter((c) => !have.has(c.id)).slice(0, N);

async function seed(c) {
  const bm = bonmun(c.id);
  if (!bm) { log(`✗ ${c.id} 본문없음`); return; }
  const img = `${REPO}/web/public${c.img}`;
  if (!existsSync(img)) { log(`✗ ${c.id} 이미지없음`); return; }
  const bf = `/tmp/seed_b_${c.id}.txt`; writeFileSync(bf, bm);
  const out = `/tmp/seed_s_${c.id}.json`;
  await new Promise((res) => { const p = spawn('node', [`${REPO}/web/scripts/gemma_measure.mjs`, img, bf, out], { stdio: ['ignore', 'ignore', 'ignore'], timeout: 180000 }); p.on('close', res); p.on('error', res); });
  if (existsSync(out)) { try { const spec = JSON.parse(readFileSync(out, 'utf8')); if (!(spec.curves || []).length && !(spec.points || []).length) { log(`✗ ${c.id} 빈spec`); return; } writeFileSync(`${SPECS}/${c.id}.json`, JSON.stringify({ id: c.id, img: c.img, spec, note: 'gemma seed' })); log(`✓ ${c.id} (곡선 ${(spec.curves || []).length})`); } catch { log(`✗ ${c.id} 파싱실패`); } }
  else log(`✗ ${c.id} gemma무응답`);
}
(async () => {
  log(`══ 시드 시작: ${cands.length}도형 · ${PAR}병렬 · LOG ${LOG}`);
  let i = 0; const w = async () => { while (i < cands.length) await seed(cands[i++]); };
  await Promise.all(Array.from({ length: PAR }, w));
  log(`══ 완료: 갤러리 총 ${readdirSync(SPECS).length}건`);
})();
