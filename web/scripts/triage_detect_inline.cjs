const fs = require('fs');
const { execSync } = require('child_process');
const matter = require('/home/insung/Projects/math-study/web/node_modules/gray-matter');
process.chdir('/home/insung/Projects/math-study');
const p = 'web/src/data/figure-triage.json';
const d = JSON.parse(fs.readFileSync(p, 'utf-8'));
const mdcache = {}, stcache = {};
function findMd(slug) {
  if (slug in mdcache) return mdcache[slug];
  let f = '';
  try { f = execSync(`find docs/problems -name "${slug}.md" 2>/dev/null`, { encoding: 'utf8' }).trim().split('\n')[0]; } catch {}
  return mdcache[slug] = f;
}
function esc(s) { return s.replace(/[{}]/g, '\\$&'); }
let n = 0, scanned = 0, undone = 0;
for (const v of Object.values(d.figures)) {
  if (v.kind !== 'figure') continue;
  // 이전 inline_shape 플래그 초기화(재실행 멱등)
  if (v.inline_shape) { delete v.inline_shape; }
  const f = findMd(v.problem_slug);
  if (!f || !fs.existsSync(f)) continue;
  let st = stcache[f];
  if (st === undefined) {
    try { const fm = matter.read(f).data; st = (fm.searchable_text || fm.corrected || ''); } catch { st = ''; }
    stcache[f] = st;
  }
  if (!st) continue;
  scanned++;
  const marker = `{{FIG${v.figure_index}}}`;
  if (st.indexOf(marker) < 0) continue;
  let inline = false;
  // 신뢰 신호만: 마커 직후 '모양'/'꼴'/'공통부분' = 본문에 도형 기호가 박힘(○○ 모양의 도형/활꼴/공통부분인).
  // ('NN. {{FIG}} 그림과 같이…' 같은 문제시작 블록그림은 제외)
  if (new RegExp(esc(marker) + '\\s*(모양|꼴|공통부분)').test(st)) inline = true;
  if (inline) {
    v.suggested = 'reuse';
    v.suggest_reason = "인라인 도형(본문에 박힘) → 재활용";
    v.inline_shape = true;
    n++;
  }
}
fs.writeFileSync(p, JSON.stringify(d, null, 2));
const c = {}; for (const v of Object.values(d.figures)) if (v.suggested) c[v.suggested] = (c[v.suggested] || 0) + 1;
const ex = Object.values(d.figures).filter((v) => v.inline_shape).map((v) => v.problem_slug + '#' + v.figure_index);
console.log('스캔', scanned, '· 인라인 감지', n);
console.log('분포', JSON.stringify(c));
console.log('인라인:', ex.join(', '));
