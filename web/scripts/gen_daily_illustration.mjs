// 「오늘의 개념」 그림 생성기 — 개념별로 LLM(haiku)이 손그림용 stroke 좌표(figure spec)를
// 1회 생성해 web/src/data/concept-illustrations.json 에 개념 id 로 캐시한다. 이미 있으면 건너뜀.
// 크론(자정 전)이 '내일 개념'을 미리 생성 → 아침엔 준비 완료. 실패/이상치는 캐시 안 함(폴백).
//
// 사용:  node scripts/gen_daily_illustration.mjs [dayOffset ...]
//   인자 없음 = [1](내일). 시드: node scripts/gen_daily_illustration.mjs 0 1 2 3 4 5 6
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { resolve, dirname } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { pickDailyConcept } from '../src/lib/daily-concept.mjs';

// ★claude -p 캐시 친화: 레포 cwd면 git status가 시스템 프롬프트 env 블록을 매 호출 바꿔 캐시를 깬다.
//   깨끗한 빈 cwd에서 실행 → prefix 안정 → 크론이 여러 개념을 연속 생성할 때 cache_read 생존(파일접근 없어 안전).
const CLEAN_DIR = process.env.CLAUDE_P_CWD || resolve(tmpdir(), 'claude_p_clean');
if (!existsSync(CLEAN_DIR)) mkdirSync(CLEAN_DIR, { recursive: true });

// 모델 — 하루 1콜(크론)이라 비용 무시 가능. 기하 품질·개념 충실도 위해 sonnet 기본.
const MODEL = process.env.FIGURE_MODEL || 'sonnet';
const WEB = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const GRAPH = resolve(WEB, 'src/data/concept-graph.json');
const CACHE = resolve(WEB, 'src/data/concept-illustrations.json');
const DAY = 86400000;

const PROMPT = (c) => `You output ONLY a JSON object (no prose, no markdown fence) describing a simple hand-drawn math figure that represents the given concept, for a small decorative sketch in a study app hero.

Schema: {"strokes":[{"pts":[x0,y0,x1,y1,...],"dash":false,"hover":false,"smooth":false}],"guideCircle":null,"equalScale":true,"blurb":"..."}
- Coordinates: world space, x in [-3,3], y in [-2,2], origin (0,0) center, +y up. USE MOST OF THE RANGE so the figure is large and clear.
- 1 to 5 strokes. Each stroke = polyline (flat list of x,y numbers). Close a shape by repeating its first point at the end.
- smooth: set TRUE for any CURVED stroke (parabola, sine, exponential, circle, ellipse, arc, bell curve, converging sequence...). For a smooth stroke give 6-12 well-spaced control points — the renderer splines them into a clean smooth curve, so do NOT try to emit many tiny segments. Set FALSE for straight-edge strokes (triangles, polygons, vectors, line segments, right-angle marks).
- equalScale: true for geometric figures (triangles, circles, polygons, angles, vectors) so they aren't squished; false for function graphs (parabola, sine, exp...).
- guideCircle: a radius number ONLY when a faint compass circle helps (e.g., circle/arc topics); else null.
- hover: true on ONE main function curve only; for geometric shapes use false everywhere.
- Make it MINIMAL, CLEAN, well-proportioned, and FAITHFUL to the concept's actual meaning (not a generic shape):
  · vector / 벡터 operations → draw real arrows WITH arrowheads (a stroke for the shaft + 2 short strokes for the head); show the operation (e.g., scalar multiple = two arrows, one longer along the same direction).
  · focus / 초점 of conic → a proper ellipse with two clearly placed focus dots inside.
  · inscribed/circumscribed → the circle and polygon actually tangent/touching.
  · sequence / limit → discrete points approaching a dashed asymptote.
  Add meaningful marks (right-angle square, arc for an angle, tick/dot for a point).
- blurb: ONE short Korean sentence (한 문장, 40자 안팎) — 이 개념의 핵심 직관이나 흥미를 끄는
  한 줄. 친근한 자연어로, 기호·전문용어 남발 금지, 학생에게 말 걸듯("…랍니다" 같은 되묻기 금지,
  평서문). 예: "직각삼각형에서는 한 각만 정해지면 세 변의 비가 전부 결정돼요."

Concept: 「${c.label}」  (단원: ${c.unit || '-'}, 과목: ${c.domain || '-'})
Output ONLY the JSON object.`;

// claude 1회 호출 + JSON 추출. timeout/파싱 실패 시 throw.
function callOnce(concept) {
  const args = ['-p', '--model', MODEL, '--output-format', 'json',
    '--disallowedTools', 'Bash,Edit,Write,Read,Glob,Grep,WebFetch,WebSearch',
    '--max-turns', '1', '--', PROMPT(concept)];
  // ★timeout 120→180s: 일부 개념은 haiku 응답이 길어 120s 초과 → ETIMEDOUT 잦았다.
  const out = execFileSync('claude', args, { encoding: 'utf-8', timeout: 180000, maxBuffer: 8 * 1024 * 1024, cwd: CLEAN_DIR, env: { ...process.env, CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS: '1' } });
  const env = JSON.parse(out);
  if (env.is_error) throw new Error('cli:' + (env.subtype || ''));
  let txt = env.result || '';
  const fence = txt.match(/```(?:json)?\s*([\s\S]*?)```/);
  if (fence) txt = fence[1];
  const obj = txt.match(/\{[\s\S]*\}/);
  if (!obj) throw new Error('no-json');
  return JSON.parse(obj[0]);
}

// ★ETIMEDOUT/일시 오류 자동 재시도(총 3회). claude 응답시간 편차로 1회 실패가 잦아
//   cron 이 폴백곡선을 남기던 문제를 흡수. 점증 대기로 부하 회피.
function callLLM(concept) {
  let lastErr;
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      return callOnce(concept);
    } catch (e) {
      lastErr = e;
      const msg = String(e && e.message || e);
      // 마지막 시도거나 재시도 무의미한 에러(쿼터 등)면 즉시 throw
      if (attempt === 3) break;
      // 5s, 12s 대기 후 재시도(ETIMEDOUT·no-json·일시 cli 오류 대상)
      execFileSync('sleep', [String(attempt === 1 ? 5 : 12)]);
      console.log(`    ↻ 재시도 ${attempt + 1}/3 (이전: ${msg.slice(0, 40)})`);
    }
  }
  throw lastErr;
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
    strokes.push({ pts: pts.slice(0, 400), dash: !!s.dash, hover: !!s.hover, smooth: !!s.smooth });
  }
  if (!strokes.length) return null;
  const out = { strokes };
  if (typeof spec.guideCircle === 'number' && Number.isFinite(spec.guideCircle)) out.guideCircle = spec.guideCircle;
  if (spec.equalScale) out.equalScale = true;
  if (typeof spec.blurb === 'string' && spec.blurb.trim()) out.blurb = spec.blurb.trim().slice(0, 120);
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
