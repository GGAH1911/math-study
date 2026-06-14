// 결정론 malformed 검사 — 전 문제를 reconstruct.ts(KaTeX)로 렌더, raw-latex 누출(파싱 실패) 검출.
// 누출 0 = 모든 출력이 KaTeX로 깨끗이 렌더(\begin{array} 포함)됨을 결정론적으로 보장.
import { renderReconstruct } from '/tmp/recon.mjs';
import fs from 'fs';
const rows = fs.readFileSync('/tmp/vision_qa/decoded_all.jsonl', 'utf8').trim().split('\n').map((l) => JSON.parse(l));
const LEAK = /\\(frac|sqrt|overline|lim|sum|prod|int|begin|cdot|times|log|ln|left|right|vec|le|ge|neq|alpha|beta|pi|theta|infty|lvert|rvert)\b|[_^]\{/;
let leak = 0; const samp = [];
for (const r of rows) {
  let h;
  try { h = renderReconstruct(r.text, {}); }
  catch (e) { leak++; if (samp.length < 10) samp.push(r.id.split('/').pop() + ' (throw)'); continue; }
  const txt = h.replace(/<annotation[^>]*>[\s\S]*?<\/annotation>/g, '').replace(/<[^>]+>/g, '');
  if (LEAK.test(txt)) { leak++; if (samp.length < 10) samp.push(r.id.split('/').pop()); }
}
console.log(`raw-latex 누출(KaTeX 파싱 실패): ${leak}/${rows.length}`);
console.log('예:', samp.join(', '));
