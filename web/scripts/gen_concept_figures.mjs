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
import { mkdirSync, existsSync as _existsSync } from 'node:fs';
import { tmpdir } from 'node:os';

// ★claude -p 캐시 친화: 레포 cwd면 git status가 시스템 프롬프트 env 블록을 매 호출 바꿔 캐시를 깬다.
//   깨끗한 빈 cwd에서 spawn → prefix 안정 → 여러 개념 연속 생성 시 cache_read 생존. (docs/CLAUDE_P_CACHING.md)
const CLEAN_DIR = process.env.CLAUDE_P_CWD || resolve(tmpdir(), 'claude_p_clean');
if (!_existsSync(CLEAN_DIR)) mkdirSync(CLEAN_DIR, { recursive: true });

// 백엔드: 'claude'(Haiku, 구독 한도) | 'agy'(Antigravity CLI, Google AI Pro 쿼터 — 별도 풀).
// agy 는 --output-format json 이 없어 plain text 를 내므로 parseEnvelope 로 직접 추출한다.
const BACKEND = process.env.LLM_BACKEND || 'claude';
const MODEL = process.env.FIGURE_MODEL ||
  (BACKEND === 'agy' ? 'Gemini 3.5 Flash (Medium)' : 'haiku'); // 사용자 지침: 하이쿠
const WEB = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const REPO = resolve(WEB, '..');
const GRAPH = resolve(WEB, 'src/data/concept-graph.json');
// FIGURE_CACHE 로 출력 캐시 경로 오버라이드 가능 — QA 등 다른 프로세스가 메인 캐시를
// 쓰는 동안 별도 파일로 생성해 충돌(클로버) 회피용. 생성 후 메인에 머지.
const CACHE = process.env.FIGURE_CACHE ? resolve(process.env.FIGURE_CACHE) : resolve(WEB, 'src/data/concept-figures.json');
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
- {"type":"ellipse","center":[x,y],"rx":a,"ry":b,"rotation?":0}             // 이차곡선(초점·준선) 기하 전용
- {"type":"parabola","vertex":[x,y],"focus?":f,"orientation?":"up|down|left|right"}  // 이차곡선 전용·함수그래프엔 쓰지마라(아래 규칙)
- {"type":"hyperbola","center":[x,y],"a":a,"b":b,"orientation?":"horizontal|vertical"}  // 이차곡선 전용
- {"type":"parametric","x":"cos(t)","y":"sin(t)","tRange":[0,"2*pi"]}      // expr=문자열, sqrt/pi 가능. ★거듭제곱은 ^ (t^2), Python ** 금지(곡선 소실)
- {"type":"area","y":"<f(x)>","from":a,"to":b,"baseline?":0,"fill?":"#6366f1","fillOpacity?":0.22,"label?":"S"}  // 곡선과 baseline 사이 면을 **채움**(적분·넓이·부호영역). y 는 x(또는 t) 식. 두 곡선 사이는 baseline 에 아래 곡선식 문자열. ★면 설명 라벨(S, f(x)>0, 넓이 등)은 이 **label 속성**으로 — 별도 text 로 면 위에 띄우지 마라(text 는 면 중앙이 아니라 가까운 곡선에 붙어 어느 면인지 안 보인다).
- {"type":"vector","from":[x,y],"to":[x,y],"label?":"\\\\vec{v}"}            // 화살표
- {"type":"angle","at":[x,y],"from":[x,y],"to":[x,y],"label?":"\\\\theta","radius?":0.4}  // 각 라벨은 호 위에 렌더됨
- {"type":"text","at":[x,y],"text":"..."}
- {"type":"sequence","expr":"<a_n 식(변수 n)>","nRange":[1,10],"limit?":L,"labelBase?":"a","connect?":false}  // 수열/급수: n=1..N 의 점 (n,a_n) 을 **자동 생성**(점 일일이 찍지 마라). limit=수렴값(y=L 점선+라벨), labelBase=첨자(a_1,a_2.. 앞3개), connect=점 잇기. 예 a_n=2-1.8/n → expr="2-1.8/n". 부분합 S_n 도 expr 에 식.

규칙:
- showAxes: 순수 기하(삼각형·원·벡터·각)는 **false**. 함수그래프/좌표평면 개념(포물선 y=x², 그래프 위의 점, 원의 방정식)처럼 **축이 의미를 갖는 경우에만 true**.
- 최소·명료하게(shapes 2~6개). 개념의 실제 의미에 **충실**히(일반적 모양 말고).
- 각을 나타내는 변수(θ 등)는 반드시 angle shape 으로(호 위에 표시됨). 변 길이·점 이름은 segment/point label.
- 좌표는 정확한 수(또는 "sqrt(3)" 같은 평가 가능한 문자열). range/yRange 는 도형을 ~15% 여백으로 빠듯하게 감싼다.
- 라벨은 KaTeX 가능(\\\\theta, \\\\vec{v}, x^2). 한국어 텍스트 라벨도 가능.
- ★두 도형을 비교(닮음·합동·평행·대칭 등)할 때 **반드시**:
  · 도형 사이에 **넉넉한 간격**을 둔다 — 두 도형이 마주보는 꼭짓점의 라벨이 가운데 좁은 틈에 겹쳐 섞이지 않도록, 도형 사이 빈 가로 간격을 **작은 도형의 가로폭 이상**으로. (예: 작은 삼각형이 x[0,3] 이면 큰 삼각형은 x[3] 바로 옆이 아니라 x[7] 이후에서 시작.)
  · 대응 꼭짓점은 **프라임 표기**로: △ABC ∼ △A'B'C' (A↔A', B↔B', C↔C'). 알파벳을 이어서(A,B,C / D,E,F) 쓰지 말 것 — 어느 도형 라벨인지 섞여 보인다.
- 라벨이 도형 선·다른 라벨과 겹치지 않게 각 꼭짓점/요소 주위에 라벨 들어갈 여백을 남긴다.
- ★함수 그래프(y=f(x): 포물선 y=x²+1, 직선, 사인, 지수, 로그 등)는 **반드시 parametric** 으로:
  {"type":"parametric","x":"t","y":"<f(t)>","tRange":[xmin,xmax]} — 곡선이 함수와 **정확히 일치**해야
  점이 곡선 위에 놓인다. (예: y=x²+1 → {"x":"t","y":"t^2+1","tRange":[-2.2,2.2]}.) 직선 y=2x-1 →
  {"x":"t","y":"2*t-1","tRange":[...]}. parabola/ellipse/hyperbola shape 은 **초점·준선을 다루는
  이차곡선 단원 도식에서만**(focus 등 정확히 지정). 함수그래프에 쓰면 기본 폭이 달라 점이 곡선에서 뜬다.
- ★점을 곡선 위에 찍을 땐, 그 점의 좌표가 곡선식을 **정확히 만족**하는지 sympy 로 확인하고(이미 함),
  곡선도 그 식을 그대로 그리는 shape(보통 parametric)인지 확인한다 — 점은 맞는데 곡선이 다른 식이면 어긋난다.
- ★적분·넓이·영역·부호(정적분, 곡선과 x축 사이, 두 곡선 사이 넓이, 속도-시간→변위 등)는 **area shape 로 면을 채워라**.
  점선 세로줄을 여러 개 모아 영역을 흉내내지 마라(보기 싫다). 곡선은 parametric, 그 아래 영역만 area:
  {"type":"area","y":"<f(x)>","from":a,"to":b} — area 의 y 식과 곡선 parametric 의 식을 **동일하게**.
- ★수열·급수(수렴/발산, a_n→L, 부분합 S_n 의 거동)은 점을 하나씩 찍지 말고 **반드시 sequence shape** 로:
  {"type":"sequence","expr":"<a_n 또는 S_n 식(n)>","nRange":[1,10],"limit":L} — 렌더러가 (n,a_n) 점들을 자동 생성한다.
  점(point) 1~2개로 수열을 흉내내면 '수렴해 가는 모습'이 안 보여 불완전(QA 탈락). 수렴값 있으면 limit 로 점선 표시.
- ★**가독성(중요)**: 주석을 다는 핵심 요소(점 P·반지름 r·각 θ 등)는 화면에서 **충분히 크게·서로 떨어져** 보여야 한다.
  · 큰 곡선(나선·긴 그래프) 위의 점 P 는 원점 근처(작은 r)가 아니라 **화면 크기에 견줄 만한 위치**에 둬라.
    예: 나선 r=θ 에서 P 를 r≈1 에 두면 곡선은 r≈6 까지 뻗어 점·각·라벨이 가운데 한 점에 뭉쳐 안 보인다 →
    P 를 θ≈4(r≈4) 처럼 크게, 또는 range 를 P 가 화면의 상당 부분을 차지하게 좁혀라(곡선 전체를 다 담을 필요 없음).
  · O·P·r·θ 같은 라벨이 좁은 영역에 겹치지 않게 요소 간 간격 확보. 한 점에 라벨 3개 이상 뭉치면 배치 실패다.
- ★명확한 2D 도식을 만들기 어려운 추상·고급 개념(또는 핵심이 3D/대수적)인 경우 억지로 그리지 말고 figure:null 로.

★★ 자가점검 5항목 — QA 수정의 80%가 여기서 나온다. 출력 전 반드시 확인:
1) showAxes: **좌표가 의미를 갖는 개념이면 반드시 true**. 해당: 단위원(cos θ=x·sin θ=y), 모든 함수그래프 y=f(x),
   좌표평면 위의 점·도형, 특정 방정식 예시(x²+y²=4 등), 극좌표(x=r cosθ). 순수 합동·닮음·각도관계만 false. **헷갈리면 true.**
2) 라벨 겹침 금지: 두 라벨이 같은 좌표·같은 자리에 오면 안 된다. 특히 **segment 라벨은 그 중점에 찍힌다** —
   그 중점이 어떤 point 좌표와 같거나 다른 라벨과 겹치면 segment label 을 빼거나 위치를 바꿔라. 한 점 주위 라벨 3개+ 금지.
3) range: **모든 도형을 여유 10~15%로 딱 감싸게**. 대칭 도형(단위원)은 대칭 range(예 [-1.2,1.2]). parametric tRange 가
   만드는 곡선 끝점까지 range 안에 들어오게(y=x², t∈[-3,3] → y=9까지 → yRange 반영). 도형이 화면 25%만 차지하면 실패.
4) 핵심 요소엔 라벨 필수: 교점·이름있는 도형(C₁,C₂)·단위원 반지름=1·sin/cos 선분·중요 좌표값 등 개념의 산출물은 전부 라벨.
   무표지 점만 두지 마라.
5) 충실성: 개념을 그 자체로 식별 가능하게. 쌍곡선은 **두 가지(branch) 모두**, 평행사변형 법칙은 **평행사변형 완성**(점선 포함),
   곡선은 그리려는 식의 **전 구간**(parametric tRange 가 한쪽만 그리면 안 됨). 구 등 3D 핵심이면 figure:null.

개념: 「${c.label}」  (단원 ${c.unit || '-'}, 과목 ${c.domain || '-'}, 학년 ${c.grade || '-'}, type ${c.concept_type})
본문 발췌: ${body || '(본문 없음)'}`;

// 쿼터 한도 자동 재개: agy 콜이 쿼터/한도 에러면 일정 간격으로 재시도(리필 대기).
// 멱등(done 스킵)이라 안전. PROBE/MAXWAIT 는 env 로 조정. 정확한 시그니처는 첫 관측 시 정규식 튜닝.
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

function callLLM(c, body) {
  const prompt = PROMPT(c, body);
  return BACKEND === 'agy' ? withQuotaRetry(() => callAgy(prompt)) : callClaude(prompt);
}

// Claude (Haiku) — --output-format json 래퍼에서 result 추출.
//   parser: result 텍스트 → envelope 추출기(기본 2D parseEnvelope, 3D는 parse3dEnvelope).
//   model: 모델 오버라이드(3D 재처리 시 sonnet).
function callClaude(prompt, parser = parseEnvelope, model = MODEL) {
  const args = ['-p', '--model', model,
    '--output-format', 'json',
    '--allowedTools', 'Bash',
    '--disallowedTools', 'Read,Write,Edit,Glob,Grep,WebFetch,WebSearch',
    '--max-turns', '20',
    '--no-session-persistence',
    '--', prompt];
  return new Promise((res, rej) => {
    const child = spawn('claude', args, { stdio: ['ignore', 'pipe', 'pipe'], cwd: CLEAN_DIR, env: { ...process.env, CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS: '1' } });
    child.stdout.setEncoding('utf8'); child.stderr.setEncoding('utf8'); // 멀티바이트(한글) 청크경계 깨짐 방지
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
        res(parser(env.result || ''));
      } catch (e) { rej(e); }
    });
  });
}

// Antigravity CLI(agy) — plain text stdout. 도구(Bash) 미부여: 순수 추론으로 figure JSON 만 생성하고
// 좌표 검증은 모델 밖(우리 sympy/완전성 게이트 + Sonnet QA)에서 결정적으로 한다(권한 게이트 해제 불필요).
// 도구 트레이스가 섞여도 parseEnvelope 가 figure 객체만 추출한다.
function callAgy(prompt) {
  // -p/--print 는 프롬프트 텍스트를 값으로 받는다(불리언 아님) → 프롬프트는 -p 바로 뒤.
  const args = ['-p', prompt,
    '--model', MODEL,
    '--print-timeout', '4m'];
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
      // ★쿼터 소진 시 agy 는 exit 0 + **빈 출력**을 낸다(에러메시지 없음). 빈 출력=쿼터/한도로
      // 간주해 withQuotaRetry 가 재시도하도록 quota 태그 에러를 던진다.
      if (!out.trim()) return rej(new Error('quota-empty: agy 빈 출력(쿼터/한도 추정)'));
      try { res(parseEnvelope(out)); } catch (e) { rej(e); }
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
  for (const s of fig.shapes.slice(0, 36)) {
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
      case 'sequence': ok = typeof s.expr === 'string' && Array.isArray(s.nRange) && s.nRange.length === 2; break;
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
  else if (bools.has('--only-3d')) {
    // 3D 개념만(Geometry3D 파동). 2D 미생성분은 안 건드림.
    const nodes = graph.nodes.filter((n) => is3D(n) && (!domain || n.id.startsWith(`${domain}/`) || n.domain === domain));
    console.log(`(3D/공간 전용 모드: ${nodes.length}개)`);
    targets = nodes.map((n) => n.id);
  }
  else if (bools.has('--all') || domain) {
    let nodes = graph.nodes.filter((n) => !domain || n.id.startsWith(`${domain}/`) || n.domain === domain);
    // 3D/공간 개념은 2D Geometry 로 표현 불가 → 전부 null 로 낭비. 기본 제외(--include-3d 로 포함).
    // (추후 Geometry3D 로 별도 파동.) 명시 ids 모드에선 필터 안 함.
    if (!bools.has('--include-3d')) {
      const before = nodes.length;
      nodes = nodes.filter((n) => !is3D(n));
      const skipped = before - nodes.length;
      if (skipped) console.log(`(3D/공간 ${skipped}개 제외 — Geometry3D 별도 파동. --include-3d 로 포함)`);
    }
    targets = nodes.map((n) => n.id);
  } else {
    console.error('대상 없음. <id...> 또는 --pilot / --all / --domain <d> [--limit N] [--concurrency N] [--include-3d] 지정.');
    process.exit(1);
  }
  return { byId, targets: targets.slice(0, Number.isFinite(limit) ? limit : undefined), force: bools.has('--force'), concurrency };
}

// 명백한 3D/공간 개념 판별 — 2D Geometry 로는 정확히 못 그려 항상 null.
//   --include-3d 없으면 제외(2D 파동), 있으면 Geometry3D(geometry3d 블록)로 생성한다.
const UNIT_3D = new Set(['입체도형', '공간도형과 공간벡터']);
const KW_3D = /공간|입체|사면체|정사면체|다면체|정육면체|직육면체|원기둥|원뿔|구면|구의\s|이면각|삼수선|정사영|평면의\s*방정식|공간벡터|교선|겉넓이|부피/;
function is3D(n) {
  return UNIT_3D.has(n.unit) || KW_3D.test(n.label || '') || KW_3D.test(n.id || '');
}

// ── 3D(입체) 도식 프롬프트 — 파일럿 검증본(6/6 ≥45). 2D gen 교훈 반영(primitive 명시·강제, 좌표정확). ──
const GEMMA3D_URL = process.env.GEMMA_URL || 'http://100.79.230.49:8080/v1/chat/completions';
const PROMPT3D = (c, body) => `너는 한국 수학 학습앱 **개념 노드**에 들어갈 **3D(입체) 도식**을 만든다.
R3F(three.js)로 렌더되며 사용자가 회전시켜 본다. 좌표가 **정확**해야 한다(정육면체는 실제 정육면체, 수직은 실제 90°, 점은 실제 곡면 위).

개념: 「${c.label}」 (단원: ${c.unit || '-'})
${body ? '참고 본문:\n' + body.slice(0, 800) : ''}

진행(단계별 사고):
STEP A — 이 개념에 3D 도식이 의미 있게 도움 되는가? 순수 대수/추상이면 → {"figure3d": null, "note":"<한 줄>"} 출력 종료.
STEP B — 핵심 입체 요소와 **반드시 성립할 관계**(직각·합동·점이 곡면 위·회전축)를 정한다.
STEP C — 구체 좌표를 배정한다(정확한 수 또는 "sqrt(3)" 평가가능 문자열).
STEP D — 최종 JSON 객체 **하나만** 출력(산문·코드펜스 금지).

출력 스키마:
{"figure3d": {"shapes":[...], "axes":true, "title":"<짧은 한국어 제목>"}, "note":"<한 줄>"}
또는 {"figure3d": null, "note":"<한 줄>"}

shapes 종류(좌표는 모두 [x,y,z] 수학좌표):
- {"type":"point3d","at":[x,y,z],"label?":"P","color?":"#e11"}
- {"type":"segment3d","from":[x,y,z],"to":[x,y,z],"label?":"","dashed?":false}
- {"type":"polyhedron","vertices":[[x,y,z],...],"faces":[[0,1,2,3],...],"labels?":["A",...],"fillOpacity?":0.3}  // faces=꼭짓점 인덱스. 정육면체=8정점 6면.
- {"type":"sphere","center":[x,y,z],"radius":r,"opacity?":0.4,"wireframe?":true}
- {"type":"parametricSurface","x":"u","y":"v","z":"<식>","uRange":[a,b],"vRange":[c,d]}  // 회전체 등 곡면. 식은 문자열, 거듭제곱은 ^ (Python ** 금지).
- {"type":"parametricCurve3d","x":"cos(t)","y":"sin(t)","z":"t","tRange":[0,"2*pi"]}  // 공간곡선
- {"type":"plane","origin":[x,y,z],"normal":[x,y,z],"size?":4,"opacity?":0.3,"label?":""}  // 평면(법선벡터)
- {"type":"text3d","at":[x,y,z],"text":"..."}

규칙(★2D 도식 운영 교훈 — 반드시 준수):
- **개념에 맞는 primitive를 정확히 골라라**(억지 표현 금지): 다면체=polyhedron, 구=sphere, 회전체=parametricSurface(회전식), 평면관계=plane, 벡터=segment3d(화살표 의미), 좌표점=point3d.
  · 회전체는 point다발/곡선 흉내 말고 **parametricSurface로 곡면을 채워라**. 예: y=f(x) x축회전 → x="u", y="f(u)*cos(v)", z="f(u)*sin(v)", uRange=[정의역], vRange=[0,"2*pi"].
  · 평면 위 수직관계(삼수선 등)는 plane + segment3d(수선). 점선은 보조선.
- **좌표 정확**: 정육면체는 모서리 길이 동일, 직각은 실제 90°, 점은 실제로 곡면/평면 위.
- **거듭제곱은 ^** (parametricSurface/Curve 식에서 ** 쓰면 곡면 소실).
- **라벨**: 핵심 점/벡터엔 label. 너무 많이 X(겹침). 충분히 떨어뜨려라. KaTeX 가능(\\\\alpha, \\\\vec{v}).
- **최소·명료**(shapes 2~6개, 입체는 최대 12). 개념의 실제 의미에 충실(일반 모양 X).
- axes: 좌표 자체가 의미면 true(공간좌표·벡터성분), 순수 입체(정육면체 단독)면 false 가능.
- title은 짧은 한국어.`;

// 3D envelope 추출(figure3d) — 산문/코드펜스 섞여도 균형중괄호로 객체만.
function parse3dEnvelope(text) {
  let t = String(text).replace(/```(?:json)?\s*([\s\S]*?)```/g, '$1');
  const j = t.indexOf('"figure3d"');
  if (j < 0) return null;
  const start = t.lastIndexOf('{', j);
  if (start < 0) return null;
  let depth = 0, end = -1;
  for (let k = start; k < t.length; k++) {
    if (t[k] === '{') depth++;
    else if (t[k] === '}') { depth--; if (depth === 0) { end = k; break; } }
  }
  if (end < 0) return null;
  try { return JSON.parse(t.slice(start, end + 1)); } catch { return null; }
}

const VALID_3D = new Set(['point3d', 'segment3d', 'polyhedron', 'parametricSurface', 'parametricCurve3d', 'sphere', 'plane', 'text3d']);
// 3D spec 검증 — 스키마 정합(타입·shapes·** 금지). 통과만 채택.
function sanitizeFigure3d(f) {
  if (!f || !Array.isArray(f.shapes) || f.shapes.length === 0) return null;
  if (f.shapes.some((s) => !s || !VALID_3D.has(s.type))) return null;
  if (JSON.stringify(f).includes('**')) return null;   // 거듭제곱 ** → 곡면 소실
  return { shapes: f.shapes, axes: f.axes !== false, title: (f.title || '').slice(0, 60) };
}

// gemma(맥북 로컬, 토큰0) 텍스트 생성 — 3D 기본 백엔드(파일럿서 빠르고 충분).
async function callGemma3d(prompt) {
  const body = JSON.stringify({ model: process.env.GEMMA_MODEL || 'mlx-community/gemma-4-26B-A4B-it-qat-4bit',
    messages: [{ role: 'user', content: prompt }], max_tokens: 2000, temperature: 0.2 });
  const r = await fetch(GEMMA3D_URL, { method: 'POST', headers: { 'content-type': 'application/json' }, body });
  const j = await r.json();
  return j.choices?.[0]?.message?.content || '';
}

// 3D 도식 생성 — 백엔드: gemma(기본·토큰0) / claude(FIGURE3D_BACKEND=claude, sonnet 권장). 반환 {figure3d, note}.
async function callLLM3d(c, body) {
  const prompt = PROMPT3D(c, body);
  const be = process.env.FIGURE3D_BACKEND || 'gemma';
  if (be === 'gemma') return parse3dEnvelope(await callGemma3d(prompt));
  // claude 경로(clean cwd 캐싱) — sonnet 이 교육적 부가요소 강함(파일럿 결과). parse3dEnvelope 로 figure3d 추출.
  return callClaude(prompt, parse3dEnvelope, process.env.FIGURE_MODEL || 'sonnet');
}

async function main() {
  const graph = JSON.parse(readFileSync(GRAPH, 'utf-8'));
  const { byId, targets, force, concurrency } = resolveTargets(graph);
  const cache = existsSync(CACHE) ? JSON.parse(readFileSync(CACHE, 'utf-8')) : { v: SCHEMA_VERSION, figures: {} };
  if (!cache.figures) cache.figures = {};
  const stat = { made: 0, nullFig: 0, skipped: 0, failed: 0, done: 0 };
  const N = targets.length;
  console.log(`figure 생성 시작: 대상 ${N}개 · 백엔드 ${BACKEND} · 모델 ${MODEL} · 동시성 ${concurrency}${force ? ' · FORCE' : ''}`);
  // 캐시 쓰기는 메인 스레드의 동기 블록에서만(워커 await 사이) — 동시 clobber 없음.
  const writeCache = () => writeFileSync(CACHE, JSON.stringify(cache, null, 0));

  let idx = 0;
  async function worker() {
    while (idx < targets.length) {
      const id = targets[idx++];
      const c = byId.get(id);
      const tag = () => `[${stat.done + 1}/${N}]`;
      if (!c) { console.log(`✗ ${id} — 그래프에 없음`); stat.failed++; stat.done++; continue; }
      // 멱등 스킵: 3D 개념은 figure3d 키, 2D 개념은 figure 키가 이미 있으면 스킵.
      const _cached = cache.figures[id];
      const _alreadyDone = _cached && (is3D(c) ? ('figure3d' in _cached) : ('figure' in _cached));
      if (!force && _alreadyDone) { console.log(`· ${c.label} — 이미 캐시(스킵)`); stat.skipped++; stat.done++; continue; }
      // ── 3D 개념: Geometry3D(geometry3d) 경로 — figure3d 키로 저장 ──
      if (is3D(c)) {
        try {
          const env = await callLLM3d(c, conceptBody(id));
          if (!env || !('figure3d' in env)) throw new Error('no-figure3d-field');
          if (env.figure3d === null) {
            cache.figures[id] = { ...(cache.figures[id] || {}), figure3d: null, label: c.label, note3d: (env.note || '').slice(0, 200), model3d: process.env.FIGURE3D_BACKEND || 'gemma', v: SCHEMA_VERSION };
            stat.nullFig++; console.log(`${tag()} ○ ${c.label} — 3D 도식 불필요 (${(env.note || '').slice(0, 40)})`);
          } else {
            const f3 = sanitizeFigure3d(env.figure3d);
            if (!f3) { console.log(`${tag()} ✗ ${c.label} — 무효 3D spec`); stat.failed++; stat.done++; continue; }
            cache.figures[id] = { ...(cache.figures[id] || {}), figure3d: f3, label: c.label, note3d: (env.note || '').slice(0, 200), model3d: process.env.FIGURE3D_BACKEND || 'gemma', v: SCHEMA_VERSION };
            stat.made++; console.log(`${tag()} ✓ ${c.label} — 3D figure OK (shapes ${f3.shapes.length})`);
          }
          writeCache();
        } catch (e) { console.log(`${tag()} ✗ ${c.label} — 3D 생성 실패: ${e.message}`); stat.failed++; }
        stat.done++; continue;
      }
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
