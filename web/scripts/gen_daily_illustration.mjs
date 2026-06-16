// 「오늘의 개념」 그림 생성기 — 개념별로 LLM(haiku)이 손그림용 stroke 좌표(figure spec)를
// 1회 생성해 web/src/data/concept-illustrations.json 에 개념 id 로 캐시한다. 이미 있으면 건너뜀.
// 크론(자정 전)이 '내일 개념'을 미리 생성 → 아침엔 준비 완료. 실패/이상치는 캐시 안 함(폴백).
//
// 사용:  node scripts/gen_daily_illustration.mjs [dayOffset ...]
//   인자 없음 = [1](내일). 시드: node scripts/gen_daily_illustration.mjs 0 1 2 3 4 5 6
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { pickDailyConcept } from '../src/lib/daily-concept.mjs';

const WEB = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const GRAPH = resolve(WEB, 'src/data/concept-graph.json');
const CACHE = resolve(WEB, 'src/data/concept-illustrations.json');
const DAY = 86400000;

const PROMPT = (c) => `You output ONLY a JSON object (no prose, no markdown fence) describing a simple hand-drawn math figure that represents the given concept, for a small decorative sketch in a study app hero.

Schema: {"strokes":[{"pts":[x0,y0,x1,y1,...],"dash":false,"hover":false}],"guideCircle":null,"equalScale":true}
- Coordinates: world space, x in [-3,3], y in [-2,2], origin (0,0) center, +y up. USE MOST OF THE RANGE so the figure is large and clear.
- 1 to 5 strokes. Each stroke = polyline (flat list of x,y numbers). Close a shape by repeating its first point at the end.
- equalScale: true for geometric figures (triangles, circles, polygons, angles, vectors) so they aren't squished; false for function graphs (parabola, sine, exp...).
- guideCircle: a radius number ONLY when a faint compass circle helps (e.g., circle/arc topics); else null.
- hover: true on ONE main function curve only; for geometric shapes use false everywhere.
- Make it MINIMAL, CLEAN, and clearly recognizable as the concept (add small marks like a right-angle square or an arc when meaningful).

Concept: 「${c.label}」  (단원: ${c.unit || '-'}, 과목: ${c.domain || '-'})
Output ONLY the JSON object.`;

function callLLM(concept) {
  const args = ['-p', '--model', 'haiku', '--output-format', 'json',
    '--disallowedTools', 'Bash,Edit,Write,Read,Glob,Grep,WebFetch,WebSearch',
    '--max-turns', '1', '--', PROMPT(concept)];
  const out = execFileSync('claude', args, { encoding: 'utf-8', timeout: 120000, maxBuffer: 8 * 1024 * 1024 });
  const env = JSON.parse(out);
  if (env.is_error) throw new Error('cli:' + (env.subtype || ''));
  let txt = env.result || '';
  const fence = txt.match(/```(?:json)?\s*([\s\S]*?)```/);
  if (fence) txt = fence[1];
  const obj = txt.match(/\{[\s\S]*\}/);
  if (!obj) throw new Error('no-json');
  return JSON.parse(obj[0]);
}

// figure spec 검증·정제 — 부적합 stroke 제거, 유효 stroke 1개 이상이어야 통과.
function sanitize(spec) {
  if (!spec || !Array.isArray(spec.strokes)) return null;
  const strokes = [];
  for (const s of spec.strokes.slice(0, 6)) {
    if (!s || !Array.isArray(s.pts)) continue;
    const pts = s.pts.map(Number);
    if (pts.length < 4 || pts.length % 2 !== 0) continue;
    if (!pts.every((v) => Number.isFinite(v) && Math.abs(v) <= 6)) continue;
    strokes.push({ pts: pts.slice(0, 400), dash: !!s.dash, hover: !!s.hover });
  }
  if (!strokes.length) return null;
  const out = { strokes };
  if (typeof spec.guideCircle === 'number' && Number.isFinite(spec.guideCircle)) out.guideCircle = spec.guideCircle;
  if (spec.equalScale) out.equalScale = true;
  return out;
}

function main() {
  const offsets = process.argv.slice(2).map(Number).filter((n) => Number.isFinite(n));
  const days = offsets.length ? offsets : [1];
  const graph = JSON.parse(readFileSync(GRAPH, 'utf-8'));
  const cache = existsSync(CACHE) ? JSON.parse(readFileSync(CACHE, 'utf-8')) : {};
  const now = Date.now();
  let made = 0, skipped = 0, failed = 0;
  for (const off of days) {
    const c = pickDailyConcept(graph.nodes, now + off * DAY);
    if (!c) { console.log(`day+${off}: 개념 없음`); continue; }
    if (cache[c.id]) { console.log(`day+${off}: ${c.label} — 이미 캐시(스킵)`); skipped++; continue; }
    try {
      const spec = sanitize(callLLM(c));
      if (!spec) { console.log(`day+${off}: ${c.label} — 무효 spec(폴백)`); failed++; continue; }
      cache[c.id] = { ...spec, label: c.label };
      writeFileSync(CACHE, JSON.stringify(cache, null, 0));
      made++;
      console.log(`day+${off}: ${c.label} — 생성 OK (strokes ${spec.strokes.length})`);
    } catch (e) {
      console.log(`day+${off}: ${c.label} — 생성 실패: ${e.message}`);
      failed++;
    }
  }
  console.log(`\n완료: 생성 ${made} · 스킵 ${skipped} · 실패 ${failed} · 캐시 총 ${Object.keys(cache).length}`);
}
main();
