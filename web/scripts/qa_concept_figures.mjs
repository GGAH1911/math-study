// 개념 도식 QA 검수기 — 생성된 도식을 Sonnet 비평가가 평가하고, 고칠 게 있으면 그 자리에서
// 스펙을 고쳐 concept-figures.json 에 다시 쓴다. **하이브리드 검수**:
//   (1) 고정폭 하네스(/dev/figrender)로 **실제 크기** 렌더 스샷 → Sonnet 이 눈으로 봄
//       (헤드리스 240 floor 과소측정 회피 — fixedWidth)
//   (2) 좌표·관계는 sympy(Bash)로 수치 검증
// 멱등: qa.checked 표시된 건 스킵(--force 로 재검수). 캐시 단일 writer(생성배치 종료 후 실행).
//
// 사용:
//   node scripts/qa_concept_figures.mjs --all [--concurrency N] [--limit N] [--force]
//   node scripts/qa_concept_figures.mjs <id...>            # 지정 도식만
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { spawn } from 'node:child_process';
import { resolve, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

// 백엔드: 'claude'(Sonnet, 구독 한도) | 'agy'(Antigravity CLI, Gemini vision — Google AI Pro 쿼터).
// agy 는 로컬 PNG 를 Read 도구로 자동 판독(권한 스톨 없음). 좌표 검증은 도구 없이 추론으로.
const BACKEND = process.env.QA_BACKEND || 'claude';
const MODEL = process.env.QA_MODEL || (BACKEND === 'agy' ? 'Gemini 3.5 Flash (Medium)' : 'sonnet');
// DRY=1: 수정 적용·캐시 기록 없이 첫 판정만 수집(정확도 파일럿용). 결과는 /tmp/qa_pilot_verdicts.json.
const DRY = process.env.QA_DRY === '1';
// QA_BATCH=N(>1): PASS 1 에서 N개씩 한 콜로 평가만(루브릭 1회만 전송 → 쿼터 절감).
// ok 는 그대로 통과, 결함난 것만 PASS 2(개별 수정→재검증 루프)로. 1=비활성(전부 개별).
const BATCH = Math.max(1, Number(process.env.QA_BATCH) || 1);
const WEB = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const REPO = resolve(WEB, '..');
const CACHE = resolve(WEB, 'src/data/concept-figures.json');
const PNG_DIR = '/tmp/qa_figs';
const BASE_URL = process.env.QA_BASE_URL || 'http://localhost:4323';
const CHROME = process.env.CHROME_BIN || '/home/insung/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome';
const RENDER_W = 600;

// ---- 개념 본문 발췌(.md) ----
function conceptBody(id) {
  const p = resolve(REPO, 'docs/concepts', `${id}.md`);
  if (!existsSync(p)) return '';
  let txt = readFileSync(p, 'utf-8').replace(/^---[\s\S]*?---\n/, '').replace(/```[\s\S]*?```/g, ' ').replace(/\s+/g, ' ');
  return txt.trim().slice(0, 700);
}

// ---- 고정폭 하네스 스샷 → png 경로(실패 시 null) ----
function safeName(id) { return id.replace(/[^a-zA-Z0-9가-힣]/g, '_').slice(0, 120); }
function renderFigure(id) {
  return new Promise((res) => {
    mkdirSync(PNG_DIR, { recursive: true });
    const out = join(PNG_DIR, `${safeName(id)}.png`);
    const url = `${BASE_URL}/dev/figrender?id=${encodeURIComponent(id)}&w=${RENDER_W}`;
    const args = ['--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
      '--window-size=680,640', '--virtual-time-budget=10000', `--screenshot=${out}`, url];
    const child = spawn(CHROME, args, { stdio: 'ignore' });
    const to = setTimeout(() => { try { child.kill('SIGKILL'); } catch { /* */ } res(null); }, 45000);
    child.on('close', () => { clearTimeout(to); res(existsSync(out) ? out : null); });
    child.on('error', () => { clearTimeout(to); res(null); });
  });
}

// ---- Sonnet 비평 호출 (이미지 Read + sympy Bash 허용) ----
const RUBRIC = `너는 한국 수학 개념 도식의 QA 검수자다. 도식의 **렌더 이미지**와 **JSON 스펙**을 받아 품질을 평가하고,
문제가 있으면 **고친 스펙**을 출력한다. 멀쩡한 건 절대 건드리지 마라(불필요한 변경 금지).

검수 기준:
1. 충실성(완전성 포함): 도식이 개념을 올바르게 **그리고 완전히** 표현하는가? (예: 닮음=닮은 두 도형, 단위원=원+점+각)
   ★개념이 N개 항목을 요구하면(예: '각의 종류'=예각·직각·둔각·평각·전각 5종) **N개 전부**가 각각 **완성된 형태**(변·호·라벨 다 갖춤)로 있어야 한다.
   변 없는 외톨이 점, 라벨 없는 핵심 요소, branch 한쪽만 그린 쌍곡선/그래프 = 불완전 → 반드시 전부 채워라.
2. 좌표 정확성: 곡선 위에 찍힌 점이 그 곡선식을 정확히 만족하는가? 직각·닮음비·접선·내분 등 관계가 성립하는가? (sympy)
3. primitive: 함수그래프 y=f(x)(포물선·직선·사인 등)는 parametric 으로 그렸는가? conic(parabola/ellipse/hyperbola) shape 로
   함수를 그려 곡선과 점이 어긋나지 않는가? — 어긋나면 parametric {x:"t", y:"f(t)", tRange} 로 교체.
   ★★area 전수점검: 도식이 **영역/넓이/적분/부등식영역/부호**를 표현하는데 **area shape 로 면을 안 칠했으면**(점선 세로줄 다발·점 흩뿌리기·경계선만·아예 미표시 등 **어떤 방식이든**) → 반드시 area 로 교체해 면을 색으로 채워라:
   {"type":"area","y":"<위 경계 f(x)>","from":a,"to":b,"baseline":<아래 경계: 수 또는 "g(x)">}. (예: y>(x-1)² 영역 → area y=상단값, baseline="(x-1)^2"; 곡선-x축 사이 → baseline 0.)
   부등식 영역의 **경계곡선**은 엄격(>,<)=dashed:true(점선), 등호포함(≥,≤)=실선. (경계는 parametric 으로 따로 그림 — area 는 채움만.)
4. 가독성: 라벨이 서로 겹치거나 한 점에 3개+ 뭉치지 않는가? 주석 대상(점·각·반지름)이 화면에서 충분히 크고 분리됐는가?
   (큰 곡선 위 점이 원점 근처 작은 r 에 몰려 라벨이 뭉치면 → 점을 큰 r 로 옮기거나 range 를 좁혀라.) 라벨이 도형 내부/선에 묻히지 않는가?
   두 도형 비교는 간격 넉넉히 + 프라임(A'B'C') 표기인가?
5. 축: 함수그래프·좌표평면 개념은 showAxes:true, 순수 기하(삼각형·원·벡터·각)는 false 가 적절한가?
6. 직각 표시·각 호는 렌더러가 자동 처리하니(angle shape 두 팔이 수직이면 정사각형 마커) 스펙은 그대로 둬도 된다.

★판정 기준(중요): **명백한 결함만** ok:false 로 지적하라 — 좌표/관계 오류, 핵심 요소·항목 누락(불완전),
좌표개념인데 축 누락, range 과대/과소로 도식이 미니거나 잘림, 라벨이 심하게 겹쳐 못 읽음. 이런 게 없으면
사소한 라벨 위치·눈금 라벨 부재 등은 **ok:true 로 통과**시켜라(가독성에 큰 지장 없으면 불필요한 수정 금지).

shape 스키마(좌표=수학좌표): point{at,label?,labelDir?} polygon{vertices,labels?,closed?} segment{from,to,label?,dashed?}
circle{center,radius,label?} ellipse{center,rx,ry} parabola{vertex,focus?,orientation?} hyperbola{center,a,b,orientation?}
parametric{x,y,tRange} area{y,from,to,baseline?,fill?,fillOpacity?,label?} vector{from,to,label?} angle{at,from,to,label?,radius?} text{at,text}. range/yRange/showAxes/title.

출력은 **JSON 객체 하나만**(산문·코드펜스 금지):
- 문제 없음: {"ok": true, "note": "<한 줄 근거>"}
- 고침: {"ok": false, "issues": ["<무엇이 왜 문제>", ...], "figure": {고친 전체 figure 스펙}}
고칠 때 멀쩡한 부분은 건드리지 말되 **이슈는 완전히** 해결하라 — 특히 누락/불완전(충실성)이면 빠진 요소를
**전부 완성된 형태로 추가**(점만 찍지 말고 변·호·라벨까지). figure 는 전체 스펙(shapes·range·showAxes·title)을 담아라.`;

// area 전수점검 후보: 영역/넓이/적분/부등식 키워드가 있는데 area shape 가 없는 도식 → QA 에 힌트 주입.
const AREA_KW = /영역|부등식|넓이|적분|부호|이상|이하|미만|초과|사이|이등분|색칠/;
function areaHint(c) {
  const sh = (c.figure && c.figure.shapes) || [];
  if (sh.some((s) => s.type === 'area')) return '';
  const txt = (c.label || '') + ' ' + JSON.stringify(sh);
  if (!AREA_KW.test(txt)) return '';
  return '\n⚠️[area 점검] 이 도식은 영역/넓이/부등식 관련인데 area shape 가 없다. 면을 색으로 칠해야 하는 도식이면 area 로 교체하라(점·선다발·미표시 금지). 단순 곡선/도형이라 면이 필요 없으면 그대로 둬라.';
}

function buildQAPrompt(c, body, pngPath) {
  const verify = BACKEND === 'agy'
    ? '먼저 Read 도구로 렌더 이미지를 본 뒤, 좌표·관계는 신중히 직접 계산해 확인하라(외부 도구 없음).'
    : '먼저 Read 도구로 이미지를 보고, 좌표·관계 검증이 필요하면 Bash 로 python3/sympy 를 실행해 확인하라.';
  return `${RUBRIC}

${verify}${areaHint(c)}

--- 개념 ---
「${c.label}」 (단원 ${c.unit || '-'}, 과목 ${c.domain || '-'}, 학년 ${c.grade || '-'}, type ${c.concept_type})
본문 발췌: ${body || '(없음)'}

--- 현재 도식 스펙(JSON) ---
${JSON.stringify(c.figure)}

--- 렌더 이미지 ---
먼저 Read 도구로 이 파일을 봐라(실제 크기 렌더): ${pngPath}`;
}

// 쿼터 한도 자동 재개: agy 콜이 쿼터/한도 에러면 일정 간격으로 재시도(리필 대기). 멱등이라 안전.
const _sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const QUOTA_RE = /quota|429|rate.?limit|resource.?exhaust|too many request|limit reach|usage limit|exceeded|out of/i;
async function withQuotaRetry(fn) {
  const PROBE_MS = (Number(process.env.QUOTA_PROBE_MIN) || 10) * 60e3;
  const MAX_WAIT_MS = (Number(process.env.QUOTA_MAXWAIT_H) || 6) * 3600e3;
  let waited = 0;
  for (;;) {
    try { return await fn(); }
    catch (e) {
      const msg = String((e && e.message) || e);
      if (!QUOTA_RE.test(msg) || waited >= MAX_WAIT_MS) throw e;
      console.log(`⏸ 쿼터 한도 추정("${msg.slice(0, 60)}") — ${Math.round(PROBE_MS / 60000)}분 후 재시도 (누적 ${Math.round(waited / 60000)}분)`);
      await _sleep(PROBE_MS); waited += PROBE_MS;
    }
  }
}

function callQA(c, body, pngPath) {
  const prompt = buildQAPrompt(c, body, pngPath);
  return BACKEND === 'agy' ? withQuotaRetry(() => callQAAgy(prompt)) : callQAClaude(prompt);
}

// Sonnet — Read+Bash 허용, --output-format json 래퍼에서 result 추출.
function callQAClaude(prompt) {
  const args = ['-p', '--model', MODEL, '--output-format', 'json',
    '--allowedTools', 'Read,Bash', '--disallowedTools', 'Write,Edit,Glob,Grep,WebFetch,WebSearch',
    '--add-dir', PNG_DIR, '--max-turns', '24', '--no-session-persistence', '--', prompt];
  return new Promise((res, rej) => {
    const child = spawn('claude', args, { stdio: ['ignore', 'pipe', 'pipe'] });
    child.stdout.setEncoding('utf8'); child.stderr.setEncoding('utf8'); // 멀티바이트(한글) 청크경계 깨짐 방지
    let out = '', err = '';
    const to = setTimeout(() => { try { child.kill('SIGTERM'); } catch { /* */ } rej(new Error('timeout')); }, 300000);
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

// Antigravity CLI(agy) — Gemini vision 으로 PNG 자동 Read. plain text stdout → parseEnvelope.
function callQAAgy(prompt) {
  const args = ['-p', prompt, '--model', MODEL, '--add-dir', PNG_DIR, '--print-timeout', '4m'];
  return new Promise((res, rej) => {
    const child = spawn('agy', args, { stdio: ['ignore', 'pipe', 'pipe'] });
    child.stdout.setEncoding('utf8'); child.stderr.setEncoding('utf8'); // 멀티바이트(한글) 청크경계 깨짐 방지
    let out = '', err = '';
    const to = setTimeout(() => { try { child.kill('SIGTERM'); } catch { /* */ } rej(new Error('timeout')); }, 300000);
    child.stdout.on('data', (d) => { out += d; if (out.length > 24e6) out = out.slice(-24e6); });
    child.stderr.on('data', (d) => { err += d; if (err.length > 4096) err = err.slice(-4096); });
    child.on('error', (e) => { clearTimeout(to); rej(e); });
    child.on('close', (code) => {
      clearTimeout(to);
      if (code !== 0) return rej(new Error(`exit ${code} ${err.slice(-160)}`));
      // 쿼터 소진=exit 0+빈 출력 → quota 태그로 던져 withQuotaRetry 재시도.
      if (!out.trim()) return rej(new Error('quota-empty: agy 빈 출력(쿼터/한도 추정)'));
      try { res(parseEnvelope(out)); } catch (e) { rej(e); }
    });
  });
}

// ---- 산문/코드 섞인 결과에서 {"ok"...} 균형괄호 추출 ----
function parseEnvelope(text) {
  const fences = [...text.matchAll(/```(?:json)?\s*([\s\S]*?)```/g)].map((m) => m[1]);
  for (const f of fences) { const o = tryBalanced(f); if (o) return o; }
  const o = tryBalanced(text); if (o) return o;
  throw new Error('no-json');
}
function tryBalanced(s) {
  for (let i = 0; i < s.length; i++) {
    if (s[i] !== '{') continue;
    let depth = 0, inStr = false, esc = false;
    for (let j = i; j < s.length; j++) {
      const ch = s[j];
      if (inStr) { if (esc) esc = false; else if (ch === '\\') esc = true; else if (ch === '"') inStr = false; continue; }
      if (ch === '"') inStr = true;
      else if (ch === '{') depth++;
      else if (ch === '}') { if (--depth === 0) { const cand = s.slice(i, j + 1); if (/"ok"\s*:/.test(cand)) { try { return JSON.parse(cand); } catch { /* */ } } break; } }
    }
  }
  return null;
}
// 배치 평가 결과 = JSON 배열 [{"id","ok","issues"}]. 균형 [] 추출.
function parseBatchArray(text) {
  const fences = [...text.matchAll(/```(?:json)?\s*([\s\S]*?)```/g)].map((m) => m[1]);
  for (const f of [...fences, text]) {
    for (let i = 0; i < f.length; i++) {
      if (f[i] !== '[') continue;
      let depth = 0, inStr = false, esc = false;
      for (let j = i; j < f.length; j++) {
        const ch = f[j];
        if (inStr) { if (esc) esc = false; else if (ch === '\\') esc = true; else if (ch === '"') inStr = false; continue; }
        if (ch === '"') inStr = true;
        else if (ch === '[') depth++;
        else if (ch === ']') { if (--depth === 0) { const cand = f.slice(i, j + 1); if (/"ok"\s*:/.test(cand) && /"id"\s*:/.test(cand)) { try { return JSON.parse(cand); } catch { /* */ } } break; } }
      }
    }
  }
  return null;
}

// 공용 spawn — bin 별로 출력 파싱(claude=json 래퍼, agy=plain text).
function spawnParse(bin, args, parseFn, timeoutMs = 360000) {
  return new Promise((res, rej) => {
    const child = spawn(bin, args, { stdio: ['ignore', 'pipe', 'pipe'] });
    child.stdout.setEncoding('utf8'); child.stderr.setEncoding('utf8'); // 멀티바이트(한글) 청크경계 깨짐 방지
    let out = '', err = '';
    const to = setTimeout(() => { try { child.kill('SIGTERM'); } catch { /* */ } rej(new Error('timeout')); }, timeoutMs);
    child.stdout.on('data', (d) => { out += d; if (out.length > 24e6) out = out.slice(-24e6); });
    child.stderr.on('data', (d) => { err += d; if (err.length > 4096) err = err.slice(-4096); });
    child.on('error', (e) => { clearTimeout(to); rej(e); });
    child.on('close', (code) => {
      clearTimeout(to);
      if (code !== 0) return rej(new Error(`exit ${code} ${err.slice(-160)}`));
      if (bin !== 'claude' && !out.trim()) return rej(new Error('quota-empty: agy 빈 출력(쿼터/한도 추정)')); // 쿼터=빈출력
      try {
        if (bin === 'claude') { const env = JSON.parse(out); if (env.is_error) return rej(new Error('cli:' + (env.subtype || ''))); res(parseFn(env.result || '')); }
        else res(parseFn(out));
      } catch (e) { rej(e); }
    });
  });
}

// PASS 1 배치 평가 프롬프트 — 루브릭 1회 + N개 도식(라벨·스펙·이미지경로). 수정 스펙 없이 평가만.
function buildBatchPrompt(items) {
  const verify = BACKEND === 'agy'
    ? '각 도식의 렌더 이미지를 Read 로 본 뒤, 좌표·관계를 신중히 직접 따져라(외부 도구 없음).'
    : '각 도식의 렌더 이미지를 Read 로 보고, 필요하면 Bash 로 python3/sympy 로 좌표를 확인하라.';
  const blocks = items.map((it, i) => `[도식 ${i + 1}] id="${it.id}" 「${it.label}」
스펙: ${JSON.stringify(it.figure)}
렌더 이미지(Read 로 볼 것): ${it.pngPath}${areaHint(it)}`).join('\n\n');
  return `${RUBRIC}

${verify}

★이건 **평가 패스**다 — 고친 스펙은 내지 말고, 아래 ${items.length}개 도식을 각각 위 '명백한 결함' 기준으로 평가만 하라.
출력은 **JSON 배열 하나만**(산문·코드펜스 금지): [{"id":"<그대로>","ok":true|false,"issues":["<결함 한줄>",...]}]
ok:true 면 issues 는 [] 로. id 는 위에 준 값을 글자 그대로 적어라.

${blocks}`;
}

function callQABatch(items) {
  const prompt = buildBatchPrompt(items);
  if (BACKEND === 'agy') {
    return withQuotaRetry(() => spawnParse('agy', ['-p', prompt, '--model', MODEL, '--add-dir', PNG_DIR, '--print-timeout', '6m'], parseBatchArray));
  }
  return spawnParse('claude', ['-p', '--model', MODEL, '--output-format', 'json',
    '--allowedTools', 'Read,Bash', '--disallowedTools', 'Write,Edit,Glob,Grep,WebFetch,WebSearch',
    '--add-dir', PNG_DIR, '--max-turns', '30', '--no-session-persistence', '--', prompt], parseBatchArray);
}

// ---- figure 스펙 구조 검증(생성기와 동일) ----
const EXPR_OK = /^[-+*/(). 0-9a-zA-Z_^√π]+$/;
function coordOK(v) { return typeof v === 'number' ? Number.isFinite(v) : (typeof v === 'string' && v.trim().length > 0 && EXPR_OK.test(v)); }
const pairOK = (p) => Array.isArray(p) && p.length >= 2 && coordOK(p[0]) && coordOK(p[1]);
function sanitizeFigure(fig) {
  if (!fig || !Array.isArray(fig.shapes)) return null;
  const shapes = [];
  for (const s of fig.shapes.slice(0, 12)) {
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
      case 'area': ok = typeof s.y === 'string' && coordOK(s.from) && coordOK(s.to); break;
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

function parseArgs(argv) {
  const opts = {}, ids = [], bools = new Set();
  const V = new Set(['--concurrency', '--limit']);
  for (let i = 0; i < argv.length; i++) { const a = argv[i]; if (V.has(a)) opts[a.slice(2)] = argv[++i]; else if (a.startsWith('--')) bools.add(a); else ids.push(a); }
  return { opts, ids, bools };
}

async function main() {
  const cache = existsSync(CACHE) ? JSON.parse(readFileSync(CACHE, 'utf-8')) : { figures: {} };
  const { opts, ids, bools } = parseArgs(process.argv.slice(2));
  const force = bools.has('--force');
  const conc = Math.max(1, Math.min(6, Number(opts.concurrency) || 1));
  const limit = opts.limit != null ? Number(opts.limit) : Infinity;

  let targets;
  if (ids.length) targets = ids;
  else if (bools.has('--suspect')) {
    // 불완전 수정 의심: fixed 인데 충실성/누락류 이슈가 기록된 도식 → 강화된 QA(재검증 루프)로 재검수.
    const SUS = /누락|충실|모두|전부|없[음어]|missing|일부만|만 (존재|있)|불완전|추가|branch|가지/;
    targets = Object.entries(cache.figures)
      .filter(([, v]) => v.figure && v.qa?.fixed && (v.qa.issues || []).some((s) => SUS.test(s)))
      .map(([id]) => id);
  } else { // --all: figure 있는 것 중 미검수(또는 force)
    targets = Object.entries(cache.figures).filter(([, v]) => v.figure && (force || !v.qa?.checked)).map(([id]) => id);
  }
  targets = targets.slice(0, Number.isFinite(limit) ? limit : undefined);
  const N = targets.length;
  const stat = { ok: 0, fixed: 0, failed: 0, unverified: 0, done: 0 };
  const dryResults = [];
  console.log(`QA 검수 시작: 대상 ${N}개 · 백엔드 ${BACKEND} · 모델 ${MODEL} · 동시성 ${conc}${BATCH > 1 ? ` · 배치 ${BATCH}` : ''}${DRY ? ' · DRY(검증만)' : ''}${force ? ' · FORCE' : ''}`);
  const writeCache = () => writeFileSync(CACHE, JSON.stringify(cache, null, 0));

  // ── PASS 1: 배치 평가(루브릭 1회/배치 → 쿼터 절감). ok 는 통과 기록, 결함만 PASS 2 로. ──
  // DRY 는 정확도 파일럿이라 배치 안 함(개별 첫판정 수집).
  let pass2List = targets;
  if (BATCH > 1 && !DRY && targets.length) {
    const chunks = [];
    for (let i = 0; i < targets.length; i += BATCH) chunks.push(targets.slice(i, i + BATCH));
    const flagged = [];
    let ci = 0, p1done = 0, p1ok = 0;
    async function batchWorker() {
      while (ci < chunks.length) {
        const chunk = chunks[ci++];
        const items = [];
        for (const id of chunk) {
          const entry = cache.figures[id];
          if (!entry || !entry.figure) continue;
          const png = await renderFigure(id);
          if (!png) { flagged.push(id); continue; } // 렌더 실패 → 개별에서 처리
          items.push({ id, label: entry.label, figure: entry.figure, pngPath: png });
        }
        if (!items.length) { p1done += chunk.length; continue; }
        let verdicts = null;
        try { verdicts = await callQABatch(items); } catch (e) { console.log(`  PASS1 배치 실패→개별: ${e.message}`); }
        const vById = new Map((verdicts || []).map((v) => [v.id, v]));
        for (const it of items) {
          const v = vById.get(it.id);
          if (v && v.ok) {
            cache.figures[it.id].qa = { checked: true, fixed: false, verified: true, note: 'batch-ok', model: MODEL };
            p1ok++;
          } else {
            flagged.push(it.id); // 결함 or 미파싱 → PASS 2
          }
        }
        writeCache();
        p1done += chunk.length;
        console.log(`PASS1 [${p1done}/${targets.length}] 통과 ${p1ok} · PASS2대상 ${flagged.length}`);
      }
    }
    await Promise.all(Array.from({ length: conc }, () => batchWorker()));
    stat.ok += p1ok;
    console.log(`PASS 1 완료: 통과 ${p1ok} · PASS 2(개별 수정) 대상 ${flagged.length}`);
    pass2List = flagged;
  }

  const MAX_FIX = 2;   // 수정→재검증 반복 상한
  const N2 = pass2List.length;
  let idx = 0;
  async function worker() {
    while (idx < pass2List.length) {
      const id = pass2List[idx++];
      const entry = cache.figures[id];
      if (!entry || !entry.figure) { stat.done++; continue; }
      let line;
      try {
        // 현재 캐시 스펙을 렌더해 평가(재검수면 직전 수정본이 대상).
        const evalNow = async () => {
          const png = await renderFigure(id);
          if (!png) throw new Error('render-failed');
          return callQA({ ...entry, label: entry.label }, conceptBody(id), png);
        };
        let verdict = await evalNow();
        if (DRY) {
          // 첫 판정만 수집 — 수정/캐시기록 없음(정확도 파일럿).
          dryResults.push({ id, label: entry.label, ok: !!verdict.ok, issues: (verdict.issues || []).slice(0, 6), note: (verdict.note || '').slice(0, 120) });
          if (verdict.ok) { stat.ok++; line = `✓ ${entry.label} — OK (${(verdict.note || '').slice(0, 50)})`; }
          else { stat.fixed++; line = `✎ ${entry.label} — 이슈: ${(verdict.issues || []).join(' / ').slice(0, 100)}`; }
          stat.done++; console.log(`[${stat.done}/${N2}] ${line}`); continue;
        }
        const allIssues = [];
        let fixes = 0, invalidFix = false;
        // ★수정 후 반드시 재렌더+재검증 — Sonnet 이 결함은 잡고 수정은 불완전(예: 각의
        // 종류 5종 중 일부만)했던 사례 방지. 통과(ok) 하거나 상한까지 반복.
        while (!verdict.ok && fixes < MAX_FIX) {
          const fixed = sanitizeFigure(verdict.figure);
          if (!fixed) { invalidFix = true; break; }
          entry.figure = fixed;               // 적용
          allIssues.push(...(verdict.issues || []));
          writeCache();                        // 재렌더가 새 스펙 보도록 먼저 기록
          fixes++;
          verdict = await evalNow();           // 수정본 재검증
        }
        if (fixes === 0 && verdict.ok) {
          entry.qa = { checked: true, fixed: false, verified: true, note: (verdict.note || '').slice(0, 160), model: MODEL };
          stat.ok++; line = `✓ ${entry.label} — OK`;
        } else if (verdict.ok) {
          entry.qa = { checked: true, fixed: true, verified: true, issues: allIssues.slice(0, 6), model: MODEL };
          stat.fixed++; line = `✎ ${entry.label} — 수정·재검증OK(${fixes}회): ${allIssues.join(' / ').slice(0, 70)}`;
        } else if (invalidFix && fixes === 0) {
          entry.qa = { checked: true, fixed: false, verified: false, note: 'fix-invalid', model: MODEL };
          stat.failed++; line = `✗ ${entry.label} — 수정안 무효(원본 유지)`;
        } else {
          // 수정은 적용했으나 재검증서 여전히 이슈 — 미해결 플래그.
          entry.qa = { checked: true, fixed: true, verified: false, issues: allIssues.slice(0, 6), note: '재검증 미통과', model: MODEL };
          stat.unverified++; line = `⚠ ${entry.label} — ${fixes}회 수정했으나 재검증 미통과(플래그)`;
        }
        writeCache();
      } catch (e) {
        stat.failed++;
        line = `✗ ${entry.label} — 검수 실패: ${e.message}`;
      }
      // 완료 순서로 1씩 증가하는 단조 카운터 — 동시성에서도 중복/뒤섞임 없음.
      stat.done++;
      console.log(`[${stat.done}/${N2}] ${line}`);
    }
  }
  if (N2 > 0) await Promise.all(Array.from({ length: conc }, () => worker()));
  if (DRY) {
    writeFileSync('/tmp/qa_pilot_verdicts.json', JSON.stringify(dryResults, null, 2));
    console.log(`\nDRY 완료: OK ${stat.ok} · 이슈지적 ${stat.fixed} · 실패 ${stat.failed} · (총 ${N}) → /tmp/qa_pilot_verdicts.json`);
  } else {
    console.log(`\n완료: OK ${stat.ok} · 수정·재검증OK ${stat.fixed} · 재검증미통과 ${stat.unverified} · 실패 ${stat.failed} · (총 ${N})`);
  }
}
main();
