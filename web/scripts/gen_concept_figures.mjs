// 개념 노드 figure 생성기 — 개념마다 "좌표 정확 + 축 숨김" Geometry spec 을 haiku 가
// **단계별(STEP A~D, 필요시 sympy 로 좌표 검증)** 로 1회 생성해
// web/src/data/concept-figures.json 에 개념 id 로 캐시한다. 이미 있으면 스킵(--force 로 재생성).
//
// 렌더는 Geometry.tsx (축·눈금 숨김) → 교과서 도식. 그림이 의미 없는 개념(추상·순수대수)은
// figure:null 로 캐시해 재호출을 막는다(폴백). 콘셉트 figure ≠ PaperHero 손그림(별개 캐시).
//
// 보안: 이 스크립트는 **로컬 소유자 빌드 타임 배치**다(사용자 향 /api/chat 의 샌드박스와 별개).
//   좌표 정확도(닮음비·점이 원 위·내분 등)를 위해 Bash(python3/sympy)만 허용한다.
//   Read/Write/Edit/Web 은 차단. 프롬프트 입력은 우리 DB 의 개념 라벨/본문이라 신뢰 가능.
//
// 사용:
//   node scripts/gen_concept_figures.mjs <id1> <id2> ...      # 지정 개념
//   node scripts/gen_concept_figures.mjs --pilot              # 내장 파일럿 세트
//   node scripts/gen_concept_figures.mjs --domain geometry --limit 30
//   node scripts/gen_concept_figures.mjs --all [--limit N]    # 미캐시 전체
//   옵션: --force(이미 캐시여도 재생성)  FIGURE_MODEL=sonnet(모델 오버라이드)
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { spawn } from 'node:child_process';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const MODEL = process.env.FIGURE_MODEL || 'haiku';     // 사용자 지침: 하이쿠
const WEB = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const REPO = resolve(WEB, '..');
const GRAPH = resolve(WEB, 'src/data/concept-graph.json');
const CACHE = resolve(WEB, 'src/data/concept-figures.json');
const SCHEMA_VERSION = 1;

const PILOT = [
  'functions/math-1/삼각함수/단위원_삼각함수',
  'geometry/middle-2/닮음과_피타고라스/닮음',
  'functions/middle-1/좌표평면과_그래프/선분의_내분',
  'geometry/middle-1/평면도형/이등변직각삼각형',
  'equations/high-1/방정식과_부등식/포물선과_직선의_교점',
  'geometry/geometry-elective/이차곡선/타원_접선',
  'geometry/geometry-elective/평면벡터/벡터의_합과_실수배',
  'geometry/high-1/도형의_방정식/원의_방정식',
  'geometry/middle-3/삼각비/삼각비_관계',
  'functions/math-1/삼각함수/피타고라스_삼각공식',
];

// 개념 본문 발췌(.md) — figure 충실도용. 없으면 빈 문자열.
function conceptBody(id) {
  const p = resolve(REPO, 'docs/concepts', `${id}.md`);
  if (!existsSync(p)) return '';
  let txt = readFileSync(p, 'utf-8');
  txt = txt.replace(/^---[\s\S]*?---\n/, '');                 // frontmatter 제거
  txt = txt.replace(/```[\s\S]*?```/g, ' ').replace(/\s+/g, ' '); // 코드블록·공백 압축
  return txt.trim().slice(0, 700);
}

const PROMPT = (c, body) => `너는 한국 수학 학습앱의 **개념 노드**에 들어갈 도식(diagram)을 만든다.
도식은 **좌표축·격자를 숨긴 채** 렌더되므로, 그 자체로 교과서 그림처럼 읽혀야 한다.
도형은 **좌표가 정확**해야 한다(닮음은 실제로 닮고, 직각은 실제 90°, 점은 실제로 곡선 위).

많은 개념은 도식이 불필요하다(순수 대수 항등식, 추상 정의 등). **도식이 개념 이해를
실제로 돕는 경우에만** 만든다.

진행 (단계별로 사고하고, 정확한 관계가 필요하면 Bash 로 python3/sympy 를 실행해 좌표를 검증):
STEP A — 이 개념에 2D 좌표 도식이 의미 있게 도움 되는가? 아니면 → {"figure": null, "note":"<왜 불필요한지 한 줄>"} 출력하고 종료.
STEP B — 핵심 도형 요소와 **반드시 성립해야 할 관계**를 적는다(예: 직각, 3-4-5 비, 단위원 위의 점, 2:1 내분, 접선).
STEP C — 구체 좌표를 배정하고, 그 관계를 python3/sympy 로 **수치 검증**한다(거리·점이 곡선 위·닮음비·교점). 정확해질 때까지 조정.
STEP D — 최종 JSON 만 출력(산문·코드펜스 금지).

출력 스키마(이 JSON 객체 하나만):
{"figure": {"shapes":[...], "range":[xmin,xmax], "yRange":[ymin,ymax], "showAxes":false, "title":"<짧은 한국어 제목>"}, "note":"<한 줄>"}
또는 {"figure": null, "note":"<한 줄>"}

shapes 종류(좌표는 모두 수학 좌표, 픽셀 아님):
- {"type":"point","at":[x,y],"label?":"P","labelDir?":"NE|NW|SE|SW|N|S|E|W"}
- {"type":"polygon","vertices":[[x,y],...],"labels?":["A","B","C"],"closed?":true}
- {"type":"segment","from":[x,y],"to":[x,y],"label?":"","dashed?":false}   // line=무한선 아님, 끝점-끝점
- {"type":"circle","center":[x,y],"radius":r,"label?":""}
- {"type":"ellipse","center":[x,y],"rx":a,"ry":b,"rotation?":0}
- {"type":"parabola","vertex":[x,y],"focus?":f,"orientation?":"up|down|left|right"}
- {"type":"hyperbola","center":[x,y],"a":a,"b":b,"orientation?":"horizontal|vertical"}
- {"type":"parametric","x":"cos(t)","y":"sin(t)","tRange":[0,"2*pi"]}      // expr 는 문자열, sqrt/pi 가능
- {"type":"vector","from":[x,y],"to":[x,y],"label?":"\\\\vec{v}"}            // 화살표
- {"type":"angle","at":[x,y],"from":[x,y],"to":[x,y],"label?":"\\\\theta","radius?":0.4}  // 각 라벨은 호 위에 렌더됨
- {"type":"text","at":[x,y],"text":"..."}

규칙:
- showAxes: 순수 기하(삼각형·원·벡터·각)는 **false**. 함수그래프/좌표평면 개념(포물선 y=x², 그래프 위의 점, 원의 방정식)처럼 **축이 의미를 갖는 경우에만 true**.
- 최소·명료하게(shapes 2~6개). 개념의 실제 의미에 **충실**히(일반적 모양 말고).
- 각을 나타내는 변수(θ 등)는 반드시 angle shape 으로(호 위에 표시됨). 변 길이·점 이름은 segment/point label.
- 좌표는 정확한 수(또는 "sqrt(3)" 같은 평가 가능한 문자열). range/yRange 는 도형을 ~15% 여백으로 빠듯하게 감싼다.
- 라벨은 KaTeX 가능(\\\\theta, \\\\vec{v}, x^2). 한국어 텍스트 라벨도 가능.

개념: 「${c.label}」  (단원 ${c.unit || '-'}, 과목 ${c.domain || '-'}, 학년 ${c.grade || '-'}, type ${c.concept_type})
본문 발췌: ${body || '(본문 없음)'}`;

function callLLM(c, body) {
  const args = ['-p', '--model', MODEL,
    '--output-format', 'json',
    '--allowedTools', 'Bash',
    '--disallowedTools', 'Read,Write,Edit,Glob,Grep,WebFetch,WebSearch',
    '--max-turns', '20',
    '--no-session-persistence',
    '--', PROMPT(c, body)];
  return new Promise((res, rej) => {
    const child = spawn('claude', args, { stdio: ['ignore', 'pipe', 'pipe'] });
    let out = '', err = '';
    const to = setTimeout(() => { try { child.kill('SIGTERM'); } catch { /* */ } rej(new Error('timeout')); }, 240000);
    child.stdout.on('data', (d) => { out += d; if (out.length > 24e6) out = out.slice(-24e6); });
    child.stderr.on('data', (d) => { err += d; if (err.length > 4096) err = err.slice(-4096); });
    child.on('error', (e) => { clearTimeout(to); rej(e); });
    child.on('close', (code) => {
      clearTimeout(to);
      if (code !== 0) return rej(new Error(`exit ${code} ${err.slice(-160)}`));
      try {
        const env = JSON.parse(out);
        if (env.is_error) return rej(new Error('cli:' + (env.subtype || '')));
        res(parseEnvelope(env.result || ''));
      } catch (e) { rej(e); }
    });
  });
}

// haiku 가 산문/sympy 코드 + JSON 을 섞어 내도 우리 envelope({"figure":...})만 안전 추출.
// 1) 코드펜스 우선, 2) "figure" 키를 포함하는 균형괄호 객체를 문자열 인지하며 스캔.
function parseEnvelope(text) {
  // 1) ```json ... ``` 펜스 안을 먼저 시도(여러 개면 figure 포함하는 것).
  const fences = [...text.matchAll(/```(?:json)?\s*([\s\S]*?)```/g)].map((m) => m[1]);
  for (const f of fences) {
    const o = tryBalancedFigure(f);
    if (o) return o;
  }
  // 2) 전체 텍스트에서 균형괄호 figure 객체 스캔.
  const o = tryBalancedFigure(text);
  if (o) return o;
  throw new Error('no-figure-json');
}
// "figure" 토큰을 포함하는 최외곽 균형 {..} 를 찾아 JSON.parse. 문자열 내 중괄호·이스케이프 무시.
function tryBalancedFigure(s) {
  for (let i = 0; i < s.length; i++) {
    if (s[i] !== '{') continue;
    let depth = 0, inStr = false, esc = false;
    for (let j = i; j < s.length; j++) {
      const ch = s[j];
      if (inStr) {
        if (esc) esc = false;
        else if (ch === '\\') esc = true;
        else if (ch === '"') inStr = false;
        continue;
      }
      if (ch === '"') inStr = true;
      else if (ch === '{') depth++;
      else if (ch === '}') {
        depth--;
        if (depth === 0) {
          const cand = s.slice(i, j + 1);
          if (/"figure"\s*:/.test(cand)) {
            try { return JSON.parse(cand); } catch { /* 다음 후보 */ }
          }
          break; // 이 여는 괄호에서 시작한 객체는 끝 — 다음 '{' 부터 재시도
        }
      }
    }
  }
  return null;
}

// 좌표 1개 검증: 유한 number, 또는 sqrt/pi 등 평가 가능한 문자열(렌더러 mathjs 가 풀므로 통과시킴).
const EXPR_OK = /^[-+*/(). 0-9a-zA-Z_^√π]+$/;
function coordOK(v) {
  if (typeof v === 'number') return Number.isFinite(v);
  if (typeof v === 'string') return v.trim().length > 0 && EXPR_OK.test(v);
  return false;
}
const pairOK = (p) => Array.isArray(p) && p.length >= 2 && coordOK(p[0]) && coordOK(p[1]);

// figure spec 구조 검증·정제 — 알 수 없는/깨진 shape 는 drop, 유효 shape ≥1 이어야 통과.
// (string-expr 좌표의 실제 평가/그리기는 Geometry.tsx 가 mathjs 로 수행 — 여기선 구조만.)
function sanitizeFigure(fig) {
  if (!fig || !Array.isArray(fig.shapes)) return null;
  const shapes = [];
  for (const s of fig.shapes.slice(0, 10)) {
    if (!s || typeof s.type !== 'string') continue;
    let ok = false;
    switch (s.type) {
      case 'point': case 'text': ok = pairOK(s.at); break;
      case 'polygon': ok = Array.isArray(s.vertices) && s.vertices.length >= 2 && s.vertices.every(pairOK); break;
      case 'line': case 'segment': case 'vector': ok = pairOK(s.from) && pairOK(s.to); break;
      case 'circle': ok = pairOK(s.center) && coordOK(s.radius); break;
      case 'ellipse': ok = pairOK(s.center) && coordOK(s.rx) && coordOK(s.ry); break;
      case 'hyperbola': ok = pairOK(s.center) && coordOK(s.a) && coordOK(s.b); break;
      case 'parabola': ok = pairOK(s.vertex); break;
      case 'angle': ok = pairOK(s.at) && pairOK(s.from) && pairOK(s.to); break;
      case 'parametric': ok = typeof s.x === 'string' && typeof s.y === 'string' && Array.isArray(s.tRange); break;
      default: ok = false;
    }
    if (ok) shapes.push(s);
  }
  if (!shapes.length) return null;
  const out = { shapes, showAxes: fig.showAxes === true };
  const rangeOK = (r) => Array.isArray(r) && r.length === 2 && coordOK(r[0]) && coordOK(r[1]);
  if (rangeOK(fig.range)) out.range = fig.range;
  if (rangeOK(fig.yRange)) out.yRange = fig.yRange;
  if (typeof fig.title === 'string' && fig.title.trim()) out.title = fig.title.trim().slice(0, 60);
  return out;
}

// 값을 받는 플래그(--k v)와 불리언 플래그(--force 등)를 분리 파싱. 값플래그의 값은 ids 에서 제외.
const VALUE_FLAGS = new Set(['--limit', '--domain', '--concurrency']);
function parseArgs(argv) {
  const opts = {}; const ids = []; const bools = new Set();
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (VALUE_FLAGS.has(a)) { opts[a.slice(2)] = argv[++i]; }
    else if (a.startsWith('--')) { bools.add(a); }
    else ids.push(a);
  }
  return { opts, ids, bools };
}
function resolveTargets(graph) {
  const byId = new Map(graph.nodes.map((n) => [n.id, n]));
  const { opts, ids, bools } = parseArgs(process.argv.slice(2));
  const limit = opts.limit != null ? Number(opts.limit) : Infinity;
  const domain = opts.domain ?? null;
  const concurrency = opts.concurrency != null ? Math.max(1, Math.min(8, Number(opts.concurrency) || 1)) : 1;

  let targets;
  if (ids.length) targets = ids;
  else if (bools.has('--pilot')) targets = PILOT;
  else if (bools.has('--all') || domain) {
    targets = graph.nodes
      .filter((n) => !domain || n.id.startsWith(`${domain}/`) || n.domain === domain)
      .map((n) => n.id);
  } else {
    console.error('대상 없음. <id...> 또는 --pilot / --all / --domain <d> [--limit N] [--concurrency N] 지정.');
    process.exit(1);
  }
  return { byId, targets: targets.slice(0, Number.isFinite(limit) ? limit : undefined), force: bools.has('--force'), concurrency };
}

async function main() {
  const graph = JSON.parse(readFileSync(GRAPH, 'utf-8'));
  const { byId, targets, force, concurrency } = resolveTargets(graph);
  const cache = existsSync(CACHE) ? JSON.parse(readFileSync(CACHE, 'utf-8')) : { v: SCHEMA_VERSION, figures: {} };
  if (!cache.figures) cache.figures = {};
  const stat = { made: 0, nullFig: 0, skipped: 0, failed: 0, done: 0 };
  const N = targets.length;
  console.log(`figure 생성 시작: 대상 ${N}개 · 모델 ${MODEL} · 동시성 ${concurrency}${force ? ' · FORCE' : ''}`);
  // 캐시 쓰기는 메인 스레드의 동기 블록에서만(워커 await 사이) — 동시 clobber 없음.
  const writeCache = () => writeFileSync(CACHE, JSON.stringify(cache, null, 0));

  let idx = 0;
  async function worker() {
    while (idx < targets.length) {
      const id = targets[idx++];
      const c = byId.get(id);
      const tag = () => `[${stat.done + 1}/${N}]`;
      if (!c) { console.log(`✗ ${id} — 그래프에 없음`); stat.failed++; stat.done++; continue; }
      if (!force && cache.figures[id]) { console.log(`· ${c.label} — 이미 캐시(스킵)`); stat.skipped++; stat.done++; continue; }
      try {
        const env = await callLLM(c, conceptBody(id));
        if (!env || !('figure' in env)) throw new Error('no-figure-field');
        if (env.figure === null) {
          cache.figures[id] = { figure: null, label: c.label, note: (env.note || '').slice(0, 200), model: MODEL, v: SCHEMA_VERSION };
          stat.nullFig++;
          console.log(`${tag()} ○ ${c.label} — 도식 불필요 (${(env.note || '').slice(0, 40)})`);
        } else {
          const fig = sanitizeFigure(env.figure);
          if (!fig) { console.log(`${tag()} ✗ ${c.label} — 무효 spec(폴백)`); stat.failed++; stat.done++; continue; }
          cache.figures[id] = { figure: fig, label: c.label, note: (env.note || '').slice(0, 200), model: MODEL, v: SCHEMA_VERSION };
          stat.made++;
          console.log(`${tag()} ✓ ${c.label} — figure OK (shapes ${fig.shapes.length}, axes ${fig.showAxes})`);
        }
        writeCache();
      } catch (e) {
        console.log(`${tag()} ✗ ${c.label} — 생성 실패: ${e.message}`);
        stat.failed++;
      }
      stat.done++;
    }
  }
  await Promise.all(Array.from({ length: concurrency }, () => worker()));
  console.log(`\n완료: figure ${stat.made} · null ${stat.nullFig} · 스킵 ${stat.skipped} · 실패 ${stat.failed} · 캐시 총 ${Object.keys(cache.figures).length}`);
}
main();
