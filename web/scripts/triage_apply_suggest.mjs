import { readFileSync, writeFileSync, existsSync } from 'node:fs';
const REPO = '/home/insung/Projects/math-study';
const idx = JSON.parse(readFileSync(`${REPO}/web/src/data/figure-triage.json`, 'utf-8'));
function suggest(c) {
  if (c.type === 'junk') return ['delete', '추출오류(텍스트조각)'];
  if (!c.has_math) return ['reuse', `숫자/수식 없음 (${c.type})`];
  if (c.dim === '3d') return ['redraw-3d', '수식+3D 입체'];
  return ['redraw-2d', `수식 박힘 (${c.type})`];
}
let applied = 0; const counts = {};
const NB = Number(process.argv[2] || 5);
for (let b = 1; b <= NB; b++) {
  const bf = `/tmp/fig_batch_${b}.txt`, rf = `/tmp/batch_${b}_result.json`;
  if (!existsSync(bf) || !existsSync(rf)) continue;
  const n2img = {};
  for (const ln of readFileSync(bf, 'utf-8').trim().split('\n')) {
    const [n, p] = ln.split('\t'); if (!p) continue;
    n2img[n] = '/problem-images' + p.split('/problem-images')[1];
  }
  let res;
  try { res = JSON.parse(readFileSync(rf, 'utf-8')); } catch { console.error(`batch ${b} result 파싱실패`); continue; }
  for (const c of res) {
    const img = n2img[String(c.n)];
    if (!img || !idx.figures[img]) continue;
    const [s, r] = suggest(c);
    idx.figures[img].suggested = s; idx.figures[img].suggest_reason = r;
    applied++; counts[s] = (counts[s] || 0) + 1;
  }
}
writeFileSync(`${REPO}/web/src/data/figure-triage.json`, JSON.stringify(idx, null, 2));
console.log('적용', applied, '· 제안분포', JSON.stringify(counts));
