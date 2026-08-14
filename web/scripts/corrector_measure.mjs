// measure-then-build (3D 투영판) — agy 1콜로 ①입체의 3D 논리좌표 ②투영 기저(3축 화면벡터) ③곡선 식 측정
// → buildFigure 가 투영 행렬로 3D→2D, 곡선은 parametric(투영된 식)으로 매끄럽게. 사용자 통찰: "2D 정확 → 벡터로 눕히기".
import { spawn } from 'node:child_process';
import { readFileSync, writeFileSync, readdirSync, existsSync, mkdirSync } from 'node:fs';

const REPO = process.env.MATHSTUDY_ROOT || new URL('../..', import.meta.url).pathname.replace(/\/$/, '');  // ★레포 위치 자동(이동 내성)
const MODEL = process.env.CORR_MODEL || 'Gemini 3.5 Flash (Medium)';
const FULL = !!process.env.CORR_FULL, OUT_DIR = '/tmp/corrector_full';
if (FULL) try { mkdirSync(OUT_DIR, { recursive: true }); } catch { /* */ }
let PROBLEMS;
if (FULL) {
  PROBLEMS = [];
  for (const round of readdirSync(`${REPO}/db/raw`)) {
    const imgDir = `${REPO}/db/raw/${round}/images`;
    if (!existsSync(imgDir)) continue;
    for (const f of readdirSync(imgDir)) {
      if (!f.endsWith('.png') || f.includes('_grid')) continue;
      const rest = f.startsWith(round + '_') ? f.slice(round.length + 1, -4) : f.slice(0, -4);
      const us = rest.lastIndexOf('_'); if (us < 0) continue;
      const subj = rest.slice(0, us), num = rest.slice(us + 1);
      if (/^\d+$/.test(num)) PROBLEMS.push([round, subj, num]);
    }
  }
  if (process.env.CORR_IDS) { const ids = process.env.CORR_IDS.split(',').map((x) => x.trim()); PROBLEMS = PROBLEMS.filter(([r, s, n]) => ids.includes(`${r}/${s}_${n}`)); } // 특정 문제만(검증용)
  else { const N = +(process.env.CORR_N || 20); if (PROBLEMS.length > N) { const step = PROBLEMS.length / N; PROBLEMS = Array.from({ length: N }, (_, i) => PROBLEMS[Math.floor(i * step)]); } }
  console.log(`FULL 샘플: ${PROBLEMS.length}문제`);
} else PROBLEMS = [['2020_수능', '가형', '12']];

function agyCall(prompt, imgDir, label) {
  return new Promise((res, rej) => {
    const t0 = Date.now();
    const child = spawn('agy', ['-p', prompt, '--model', MODEL, '--add-dir', imgDir, '--print-timeout', '6m'], { stdio: ['ignore', 'pipe', 'pipe'] });
    let out = '', err = '';
    child.stdout.setEncoding('utf8'); child.stderr.setEncoding('utf8');
    child.stdout.on('data', (d) => { out += d; });
    child.stderr.on('data', (d) => { err += d; });
    child.on('close', (code) => {
      const el = Math.round((Date.now() - t0) / 1000);
      if (code !== 0) return rej(new Error(`${label} exit ${code} ${err.slice(-120)}`));
      if (!out.trim()) return rej(new Error(`${label} quota-empty(빈출력=쿼터)`));
      console.log(`  · ${label} ${el}s`); res(out);
    });
  });
}
function extractJSON(text, key) {
  const fences = [...text.matchAll(/```(?:json)?\s*([\s\S]*?)```/g)].map((m) => m[1]);
  for (const f of [...fences, text]) {
    for (let i = 0; i < f.length; i++) {
      if (f[i] !== '{') continue;
      let depth = 0, inStr = false, esc = false;
      for (let j = i; j < f.length; j++) {
        const ch = f[j];
        if (inStr) { if (esc) esc = false; else if (ch === '\\') esc = true; else if (ch === '"') inStr = false; continue; }
        if (ch === '"') inStr = true; else if (ch === '{') depth++;
        else if (ch === '}') { if (--depth === 0) { const c = f.slice(i, j + 1); if (new RegExp(`"${key}"\\s*:`).test(c)) { try { return JSON.parse(c); } catch { try { return JSON.parse(c.replace(/\\(?!["\\/bfnrtu])/g, '\\\\')); } catch { /* */ } } } break; } }
      }
    }
  }
  return null;
}
function fixCtrl(s) { return typeof s === 'string' ? s.replace(/[\r\t\f\x0b\x08]/g, (ch) => '\\' + ({ '\r': 'r', '\t': 't', '\f': 'f', '\x0b': 'v', '\x08': 'b' }[ch])) : s; }

const MEASURE_SCHEMA = `measure 명세 = 입체를 "3D 논리좌표 + 투영"으로 분해한 설계도(코드가 그린다). JSON:
{
 "projection":{                  // ★각 축이 화면에서 어느 각도로 기울었는지 각도기로 재라(눕힘 정도 = 원점에서 x·y축 사잇각).
   "is3D":true,
   "origin":[ox,oy],             // 논리원점의 화면좌표(0~100)
   "axes":{                      // deg=화면 수평선(오른쪽=0°)에서 반시계 각도(위=+90·아래=음수). len=논리1당 화면픽셀(깊이축 z는 약축이라 len 작게). 평면도형이면 z 생략.
     "x":{"deg":-18,"len":9},"y":{"deg":90,"len":9},"z":{"deg":210,"len":5}
   }
 },
 "points":[{"name":"A","role":"..","xyz":[x,y,z]}],   // ★점의 3D 논리좌표(화면 아님). 예 적분축 x·높이 y·깊이 z
 "curves":[{"role":"..","eq":"t의 식(거듭제곱 ^)","range":[a,b],"along":"x","value":"y","fixed":{"z":0}}],
 "solids":[{"along":"x","range":[a,b],"base":"y","height":"z","size":"단면 한변 식(예 sqrt(e^x/(e^x+1)))","section":"square"}],
                                 // ★입체=단면 스윕. along축 따라 단면(정사각형)을 size(t) 크기로 쌓음. 모서리·단면은 코드가 자동. size=단면 한변(밑면 곡선값).
                                  // 곡선점 3D = along축에 t, value축에 eq(t), 나머지축은 fixed 상수. (예 밑면곡선: along x, value y, fixed{z:0})
 "axes":[{"name":"x","fromXyz":[0,0,0],"toXyz":[12,0,0]}],   // 축선: 3D 끝점(도형 너머로 연장). 렌더는 화살표.
 "segments":[{"from":"A","to":"B","kind":"solid|dashed|chain"}],
 "shading":[{"pts":["A","B","C","D"],"kind":"solid|hatch|translucent"}],
 "dimensions":[{"on":"..","value":".."}],
 "labels":[{"text":"..","anchorTo":"점이름","dir":"위|아래|좌|우"}]
}
★두 모서리가 만나면 같은 점 이름(같은 xyz). 곡선은 식으로(점샘플 X). 투영기저는 원본 그림의 실제 축 기울기 대로.`;

function measurePrompt(det, img) {
  return `너는 한국 수능 기출의 입체/평면 그림을 "3D 논리좌표 + 투영"으로 분해한다. 원본 이미지를 Read 로 보고 측정만 하라(그리지 마라).

핵심:
- 입체는 3D 논리 좌표계를 정하고(예: 적분축 x, 높이 y, 깊이 z), 각 점의 **3D 논리좌표 xyz**를 줘라(화면좌표 아님).
- ★투영(눕힘 정도)은 **각 축이 원점에서 화면 수평선과 이루는 각도**(각도기로 재듯, deg)로 재라. **라벨을 절대 바꾸지 마라**: x축=원본에서 'x' 글자 붙은 화살표 방향, y축='y' 화살표 방향, z축=단면이 들어가는 깊이 방향. 눕힘 정도는 원본의 x축·y축 사잇각 그대로 나오게.
- 곡선은 **식 eq(t)** 와 range, 그리고 곡선점의 3D 매개(along/value/fixed)로. 점으로 찍지 마라.
- ★입체가 "단면을 한 축 따라 쌓은 것"(예: x축 수직 정사각형 단면 입체)이면 **solids 로**: along(쌓는 축)·range·단면이 차지하는 base/height 축·size(단면 한변 식, 보통 밑면 곡선값)·section(square). 모서리·단면은 코드가 그리니 모서리를 일일이 재지 마라. (가형_12: along=x, range=[0,k], base=y, height=z, size=곡선식.)
- 평면 도형이면 zAxis=[0,0], 모든 z=0.
- ★원본이 **독립된 여러 그림**([그림1][그림2] 처럼 나란히, 또는 R₁·R₂·단계별로 따로 그려진 도형들)이면 최상위에 **"subs":[{그림1 measure}, {그림2 measure}]** 배열로 분리하라(각 서브는 자체 points·segments·solids·curves·labels, projection 은 공통이면 생략 가능). 한 화면에 겹치지 마라. 그림이 하나면 subs 없이 기존대로.
- ★**그림 존재 게이트**: 원본에 **실제 그림(도형·그래프)이 없고 텍스트·식만** 있으면 measure:null 로 하라. 그림을 상상해서 만들지 마라(없는 포물선·좌표축 생성 금지).
- ★**is3D 판정**: 평면(원·삼각형·사각형·함수그래프·좌표평면)은 **is3D:false**(zAxis 불필요). **입체(부피·다면체·원기둥·정사영·전개도)만 is3D:true**. 애매하면 false.
- ★**자유곡선**(주머니·구름·매끄러운 경계처럼 수식으로 못 쓰는 곡선)은 curves 에 **"pts":[[x,y],...]**(논리좌표 7~12점)로 주면 코드가 부드럽게 보간한다(식 eq 와 택일).
- ★입체는 **실제 비례보다 단면(폭·높이)을 과장**해 통통하게(교과서 스타일): 단면축(y/z) len 을 적분축(x) len 보다 크게 잡아 단면 형태·크기 변화가 한눈에 보이게.
- ★숨은 모서리(뒤쪽 안 보이는 선)는 segments kind:"dashed". x=k 같은 위치 표시선·연장선도 segments 로(도형 너머로 연장).
- ★원점 O 는 x·y축 교점 점(이름 "O"), labels anchorTo:"O" 로 묶어라(라벨이 교점에 붙음). 곡선식(y=..) 라벨은 곡선 끝 점, x=k 라벨은 x=k 선 끝에 anchorTo.

★★필수 수집 체크리스트(하나라도 빠뜨리면 안 됨):
  ① projection: 축 각도(deg)+len. **단면축(y/z) len > 적분축(x) len**(통통).
  ② solids: along·range[0,k]·base·height·size(곡선식)·section.
  ③ curves: 밑면 곡선을 **입체 너머로 연장**한 range(예 [-0.6, k+0.6]).
  ④ segments: 단면 변 + **숨은 모서리 dashed** + x=k 표시선.
  ⑤ labels: O(교점)·곡선식(곡선끝)·x=k.
  ⑥ points: 모든 꼭짓점 + 교점 "O".

${MEASURE_SCHEMA}

또한 결정론적 전사도 이미지와 대조해 교정(LaTeX, 백슬래시 \\\\).

--- 결정론적 전사 ---
${det}
--- 원본 이미지 ---
Read 로 볼 것: ${img}

출력은 JSON 하나만: {"measure":{...}, "corrected":"<전사 교정>", "fixes":["..."]}`;
}

// ---- measure → Geometry figure 결정적 변환 (투영 행렬) ----
function axVec(a) { if (!a) return [0, 0]; const r = (a.deg || 0) * Math.PI / 180; const L = a.len ?? 5; return [L * Math.cos(r), L * Math.sin(r)]; } // 각도(deg)+길이 → 화면벡터
function projFn(pr) {
  const o = pr.origin || [50, 50], ax = pr.axes || {};
  const X = axVec(ax.x), Y = axVec(ax.y), Z = axVec(ax.z);
  return ([x, y, z]) => [o[0] + x * X[0] + y * Y[0] + (z || 0) * Z[0], o[1] + x * X[1] + y * Y[1] + (z || 0) * Z[1]];
}
// 3D 매개곡선 → 투영된 parametric x(t),y(t) 식 문자열
function catmullRom(pts, seg = 10) { // 점샘플 → 매끄러운 보간(자유곡선)
  if (!Array.isArray(pts) || pts.length < 3) return pts || [];
  const out = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
    for (let t = 0; t < seg; t++) { const s = t / seg, s2 = s * s, s3 = s2 * s;
      out.push([0.5 * (2 * p1[0] + (-p0[0] + p2[0]) * s + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * s2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * s3),
                0.5 * (2 * p1[1] + (-p0[1] + p2[1]) * s + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * s2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * s3)]); } }
  out.push(pts[pts.length - 1]);
  return out;
}
function curveParam(c, pr) {
  const o = pr.origin || [50, 50], ax = pr.axes || {};
  const X = axVec(ax.x), Y = axVec(ax.y), Z = axVec(ax.z);
  const A = c.along || 'x', V = c.value || 'y', fx = c.fixed || {};
  const E = `(${String(c.eq || '0').replace(new RegExp(`(?<![a-zA-Z])${A}(?![a-zA-Z])`, 'g'), 't')})`; // eq의 along변수(x 등) → 매개 t
  const comp = (ax) => ax === A ? 't' : ax === V ? E : `(${fx[ax] ?? 0})`;
  const X3 = comp('x'), Y3 = comp('y'), Z3 = comp('z');
  const lin = (i) => `${o[i]}+(${X3})*(${X[i]})+(${Y3})*(${Y[i]})+(${Z3})*(${Z[i]})`;
  return { type: 'parametric', x: lin(0), y: lin(1), tRange: c.range || [0, 1] };
}
function evalAt(expr, t) { try { return Function('t', 'with(Math){return ' + String(expr).replace(/\be\b/g, 'E').replace(/\^/g, '**') + '}')(t); } catch { return 0; } }
// 입체 = 단면 스윕: along축 따라 단면(정사각형)을 size(t)로 스윕 → 모서리 4곡선 + 단면 polygon 자동
function buildSolid(sd, pr) {
  const out = []; if (!sd) return out;
  const A = sd.along || 'x', B = sd.base || 'y', H = sd.height || 'z', rg = sd.range || [0, 1], a = rg[0], b = rg[1];
  const szT = `(${String(sd.size || '1').replace(new RegExp(`(?<![a-zA-Z])${A}(?![a-zA-Z])`, 'g'), 't')})`;
  const o = pr.origin || [50, 50], ax = pr.axes || {}, X = axVec(ax.x), Y = axVec(ax.y), Z = axVec(ax.z);
  const corners = [[0, 0], [1, 0], [1, 1], [0, 1]]; // (base비율, height비율) — 정사각형 4모서리
  const setC = (p, axis, v) => { p[axis === 'x' ? 0 : axis === 'y' ? 1 : 2] = v; };
  for (const [bu, hu] of corners) { // 모서리 4곡선(parametric)
    if (hu === 0) continue; // 밑면 모서리 스킵: 밑앞(0,0)=x축과 중복, 밑뒤(1,0)=곡선 연장판이 대체
    const comp = (axis) => axis === A ? 't' : axis === B ? `(${bu})*${szT}` : axis === H ? `(${hu})*${szT}` : '0';
    const lin = (i) => `${o[i]}+(${comp('x')})*(${X[i]})+(${comp('y')})*(${Y[i]})+(${comp('z')})*(${Z[i]})`;
    out.push({ type: 'parametric', x: lin(0), y: lin(1), tRange: [a, b] }); // 가로 모서리(점선은 measure segments 의 dashed 가 담당)
  }
  const proj = projFn(pr);
  // 입체 겉면(반투명) — 한 모서리에서 인접 모서리까지 along 따라 스윕한 면 4개(앞·뒤·윗·밑)
  const N = 16;
  const sweepEdge = (bu, hu) => Array.from({ length: N + 1 }, (_, i) => { const t = a + (b - a) * i / N; const s = evalAt(szT, t); const p = [0, 0, 0]; setC(p, A, t); setC(p, B, bu * s); setC(p, H, hu * s); return proj(p); });
  const faces = [[[0, 0], [0, 1]], [[1, 0], [1, 1]], [[0, 1], [1, 1]], [[0, 0], [1, 0]]]; // 앞(base0)·뒤(base1)·윗(h1)·밑(h0)
  for (const [c1, c2] of faces) { const e1 = sweepEdge(c1[0], c1[1]), e2 = sweepEdge(c2[0], c2[1]); out.push({ type: 'polygon', vertices: [...e1, ...e2.slice().reverse()], closed: true, fill: '#cfcfcf', fillOpacity: 0.16, stroke: 'none' }); } // 면은 fill만(stroke 없음=두 줄 방지)
  for (const t of [a, (a + b) / 2, b]) { // 단면 polygon(시작·중간·끝)
    const s = evalAt(szT, t);
    const pts = corners.map(([bu, hu]) => { const p = [0, 0, 0]; setC(p, A, t); setC(p, B, bu * s); setC(p, H, hu * s); return proj(p); });
    out.push({ type: 'polygon', vertices: pts, closed: true, fill: '#cfcfcf', fillOpacity: 0.26, stroke: 'none' }); // 단면 변은 measure segments 가 그림(두 줄 방지)
  }
  // ★밑면 곡선(base max·height0)을 range 너머로 연장 — Gemini 가 곡선 연장을 빠뜨려도 코드가 자동으로
  const ext = (b - a) * 0.42; // 곡선식 leader 가 x=k 수직 모서리에 안 겹치게 충분히 연장
  const bc = (axis) => axis === A ? 't' : axis === B ? szT : '0';
  const bl = (i) => `${o[i]}+(${bc('x')})*(${X[i]})+(${bc('y')})*(${Y[i]})+(${bc('z')})*(${Z[i]})`;
  out.push({ type: 'parametric', x: bl(0), y: bl(1), tRange: [a - ext, b + ext] });
  return out;
}
// 측정 서브에이전트 스키마 편차 정규화 → buildOne 이 기대하는 필드로(점은 렌더 안 됨=synthetic anchor 안전).
//   axes from/to(좌표)→fromXyz/toXyz · segments fromXyz/toXyz(좌표)→synthetic point+from/to ·
//   labels anchorTo[좌표]→at[좌표] · curves points→pts.
function normalizeMeasure(m) {
  if (!m || typeof m !== 'object') return m;
  m.points = m.points || []; let syn = 0;
  const addPt = (xyz) => { const n = '__s' + (syn++); m.points.push({ name: n, xyz }); return n; };
  for (const a of m.axes || []) { if (Array.isArray(a.from) && !a.fromXyz) a.fromXyz = a.from; if (Array.isArray(a.to) && !a.toXyz) a.toXyz = a.to; }
  for (const c of m.curves || []) { if (Array.isArray(c.points) && !c.pts) c.pts = c.points.map((p) => [p[0], p[1]]); }
  for (const s of m.segments || []) { if (Array.isArray(s.fromXyz) && s.from == null) s.from = addPt(s.fromXyz); if (Array.isArray(s.toXyz) && s.to == null) s.to = addPt(s.toXyz); }
  // 라벨 앵커 좌표(anchorTo/at/anchor 가 [x,y,z])→synthetic point+anchorTo(name) 으로(buildOne 이 proj 거쳐 투영좌표로 렌더, 논리좌표 그대로 쓰던 버그 차단)
  for (const l of m.labels || []) { const a = Array.isArray(l.anchorTo) ? l.anchorTo : Array.isArray(l.at) ? l.at : Array.isArray(l.anchor) ? l.anchor : null; if (a) { l.anchorTo = addPt(a); delete l.at; delete l.anchor; } }
  // scale(논리1당 픽셀)을 별도로 주면 종횡비용 len 으로(서브에이전트가 len 을 총길이로 오해하는 케이스 보정)
  if (m.scale && m.projection && m.projection.axes) { if (m.scale.x && m.projection.axes.x) m.projection.axes.x.len = m.scale.x; if (m.scale.y && m.projection.axes.y) m.projection.axes.y.len = m.scale.y; }
  return m;
}

function buildOne(m) {
  m = normalizeMeasure(m);
  const pr = m.projection || { origin: [50, 50], axes: { x: { deg: -25, len: 14 }, y: { deg: 35, len: 12 }, z: { deg: 90, len: 14 } } };
  if (pr.axes && pr.axes.x && pr.axes.y) { const yl = pr.axes.y.len || 12; if ((pr.axes.x.len || 12) < yl * 0.85) pr.axes.x.len = Math.round(yl * 0.85); } // aspect 가드: 적분축이 단면축 대비 너무 짧으면 보정(답답 방지)
  const proj = projFn(pr);
  const P = {};
  const PX = {};
  for (const p of m.points || []) if (p && p.name && Array.isArray(p.xyz)) { P[p.name] = proj(p.xyz); PX[p.name] = p.xyz; }
  const shapes = [];
  if (!(m.solids || []).length) for (const sh of m.shading || []) { const vs = (sh.pts || []).map((n) => P[n]).filter(Boolean); if (vs.length >= 3) shapes.push({ type: 'polygon', vertices: vs, closed: true, fill: sh.kind === 'hatch' ? '#b8b8b8' : '#cfcfcf', fillOpacity: sh.kind === 'translucent' ? 0.3 : 0.55 }); } // 입체면 음영은 buildSolid 면/단면 fill 이 담당(measure.shading 중복=회색 띠 방지)
  if (!(m.solids || []).length) for (const c of m.curves || []) { try {
    if (Array.isArray(c.pts) && c.pts.length >= 2) { const scr = c.pts.map((p) => proj([p[0], p[1], p[2] || 0])); shapes.push({ type: 'polygon', vertices: catmullRom(scr), closed: !!c.closed }); } // 자유곡선=점샘플 Catmull-Rom 보간
    else shapes.push(curveParam(c, pr));
  } catch { /* */ } } // 입체면 밑면곡선=buildSolid 연장판이 그림(중복 방지)
  for (const sd of m.solids || []) { try { for (const sh of buildSolid(sd, pr)) shapes.push(sh); } catch { /* */ } } // 입체 단면 스윕
  const onAxis = (a, b) => { const e = 0.06, z = (p) => Math.abs(p[2] || 0) < e; // 두 점이 같은 좌표축 위면 축 vector 와 중복
    if (Math.abs(a[0]) < e && z(a) && Math.abs(b[0]) < e && z(b)) return true; // y축(x=0,z=0)
    if (Math.abs(a[1]) < e && z(a) && Math.abs(b[1]) < e && z(b)) return true; // x축(y=0,z=0)
    return false; };
  for (const s of m.segments || []) { if (!P[s.from] || !P[s.to]) continue; if (PX[s.from] && PX[s.to] && onAxis(PX[s.from], PX[s.to])) continue; // 좌표축과 겹치는 선 스킵(축 vector 가 그림)
    shapes.push({ type: 'segment', from: P[s.from], to: P[s.to], ...(s.kind === 'dashed' ? { dashed: true } : {}) }); }
  for (const a of m.axes || []) { const f = a.fromXyz ? proj(a.fromXyz) : P[a.from]; const t = a.toXyz ? proj(a.toXyz) : a.toward; if (f && t) shapes.push({ type: 'vector', from: f, to: t }); }
  const DIR = { '위': [0, 4], '아래': [0, -4], '좌': [-6, 0], '우': [6, 0], '좌하': [-5, -4], '우하': [5, -4], '좌상': [-5, 4], '우상': [5, 4] };
  // 곡선식 라벨은 밑면 곡선 끝(연장)에 코드가 자동 anchor — Gemini 가 곡선 위 아닌 임의점을 줘도 무시
  const sd0 = (m.solids || [])[0]; let curveEnd = null;
  if (sd0) { const A = sd0.along || 'x', B = sd0.base || 'y', rg = sd0.range || [0, 1], ext = (rg[1] - rg[0]) * 0.42, te = rg[1] + ext;
    const szT = `(${String(sd0.size || '1').replace(new RegExp(`(?<![a-zA-Z])${A}(?![a-zA-Z])`, 'g'), 't')})`;
    const s = evalAt(szT, te); const p = [0, 0, 0]; p[A === 'x' ? 0 : A === 'y' ? 1 : 2] = te; p[B === 'x' ? 0 : B === 'y' ? 1 : 2] = s; curveEnd = proj(p); }
  for (const l of m.labels || []) {
    const isCurve = /sqrt|frac/.test(l.text || '');
    const b = (isCurve && curveEnd) ? curveEnd : (P[l.anchorTo] || (Array.isArray(l.at) ? l.at : null)); if (!b) continue;
    const d = DIR[l.dir] || [0, 3];
    if (l.anchorTo === 'O' || (isCurve && curveEnd)) { shapes.push({ type: 'point', at: b, color: 'transparent', label: l.text, labelDir: l.anchorTo === 'O' ? 'SW' : 'E' }); } // 교점/곡선끝에 보이지 않는 점 → 라벨 leader 자동
    else shapes.push({ type: 'text', at: [b[0] + d[0], b[1] + d[1]], text: l.text });
  }
  for (const sh of shapes) { if (sh.type === 'polygon') { if (sh.stroke !== 'none') sh.stroke = '#1f1f1f'; } else if (sh.type !== 'text') sh.color = sh.color || '#1f1f1f'; } // 전체 검은(원본 선색)
  const RK = (sh) => sh.type === 'polygon' ? 0 : sh.type === 'text' ? 2 : 1; // 음영(polygon) 아래·선 위·라벨 맨위 → 모서리가 면 위(입체감)
  shapes.sort((a, b) => RK(a) - RK(b));
  return { shapes, range: [0, 100], yRange: [0, 100], showAxes: false, title: '' };
}
// 다중 서브그림: m.subs(원본 [그림1][그림2] 분리)면 각 서브 → figures 배열, 아니면 단일 figure
function buildFigure(m) {
  if (Array.isArray(m.subs) && m.subs.length) return { figures: m.subs.map((s) => buildOne(s.projection ? s : { ...s, projection: m.projection })) };
  return { figure: buildOne(m) };
}

async function run([round, subj, num]) {
  const id = `${round}/${subj}_${num}`;
  const outF = `${OUT_DIR}/${round}_${subj}_${num}.json`;
  if (FULL && existsSync(outF)) { console.log(`· skip ${id}(이미)`); try { return JSON.parse(readFileSync(outF, 'utf8')); } catch { /* */ } }
  const meta = `${REPO}/db/raw/${round}/meta_cache/${subj}_${num}.json`;
  const img = `${REPO}/db/raw/${round}/images/${round}_${subj}_${num}.png`;
  const imgDir = `${REPO}/db/raw/${round}/images`;
  let det = '';
  try { det = JSON.parse(readFileSync(meta, 'utf-8')).meta.searchable_text; } catch (e) { return { id, error: 'meta: ' + e.message }; }
  console.log(`▶ ${id} measure-then-build(3D)`);
  try {
    const out = await agyCall(measurePrompt(det, img), imgDir, 'measure');
    const parsed = extractJSON(out, 'measure');
    if (!parsed) { console.log(`✗ ${id} parse-fail · len${out.length} raw: ${String(out).slice(0, 140).replace(/\s+/g, ' ')}`); return { id, error: 'measure parse-fail', rawHead: out.slice(0, 200) }; }
    const measure = parsed.measure || { points: [] }; // measure:null = 그림 없는 문제(정상 → figure 빈)
    const built = buildFigure(measure); // {figure} 또는 {figures:[...]}(다중 서브그림)
    const allSh = built.figures ? built.figures.reduce((n, f) => n + (f.shapes || []).length, 0) : (built.figure?.shapes || []).length;
    const pr = measure.projection || {};
    console.log(`✓ ${id} shapes ${allSh}${built.figures ? ` · 서브${built.figures.length}` : ''} · pts ${(measure.points || []).length}·3D ${pr.is3D}`);
    const res = { id, det, measure, ...built, corrected: fixCtrl(parsed.corrected), fixes: parsed.fixes || [], figureNote: built.figures ? `다중 서브그림 ${built.figures.length}개` : '3D 투영판: 측정→투영행렬·곡선 parametric' };
    if (FULL) writeFileSync(outF, JSON.stringify(res));
    return res;
  } catch (e) { console.log(`✗ ${id}: ${e.message}`); return { id, error: e.message }; }
}

if (process.env.CORR_REBUILD) { // measure 만 고쳐 agy 없이 figure 재생성(빠른 반복·내 손 골든)
  const arr = JSON.parse(readFileSync('/tmp/corrector_sample.json', 'utf8'));
  for (const r of arr) if (r.measure) { delete r.figure; delete r.figures; Object.assign(r, buildFigure(r.measure)); }
  writeFileSync('/tmp/corrector_sample.json', JSON.stringify(arr, null, 2));
  console.log('REBUILD: measure→figure 재생성 완료'); process.exit(0);
}
console.log(`measure-then-build(3D): ${PROBLEMS.length}문제 · ${MODEL} · 동시${FULL ? 20 : 1}`);
const results = [];
const CONC = +(process.env.CORR_CONC || (FULL ? 20 : 1)); // 동시(기본 20, CORR_CONC 로 조정)
let _i = 0;
async function _w() { while (_i < PROBLEMS.length) { const k = _i++; try { results[k] = await run(PROBLEMS[k]); } catch (e) { results[k] = { id: PROBLEMS[k].join('/'), error: e.message }; console.log(`✗ ${PROBLEMS[k].join('/')}: ${e.message}`); } } }
await Promise.all(Array.from({ length: CONC }, _w));
if (!FULL) writeFileSync('/tmp/corrector_sample.json', JSON.stringify(results, null, 2));
const ok = results.filter((r) => !r.error).length;
console.log(`\n완료: ${ok}/${results.length} → /tmp/corrector_sample.json`);
results.filter((r) => r.error).forEach((r) => console.log(`  ✗ ${r.id}: ${r.error}`));
