// Geometry renderer — declarative SVG built from a small JSON spec so
// the LLM doesn't have to hand-calculate coordinates.
//
// Used via:
//
//   ```geometry
//   {
//     "shapes": [
//       {"type":"polygon","vertices":[[0,0],[4,0],[2,3]],"labels":["A","B","C"]},
//       {"type":"circle","center":[2,1],"radius":1.5,"label":"O"},
//       {"type":"point","at":[3,4],"label":"P"},
//       {"type":"vector","from":[0,0],"to":[3,4],"label":"\\vec{v}"},
//       {"type":"angle","at":[0,0],"from":[1,0],"to":[0.7,0.7],"label":"\\theta","radius":0.6}
//     ],
//     "range":[-5,5], "yRange":[-3,5],
//     "showAxes":true, "showGrid":true, "title":"직각삼각형"
//   }
//   ```
//
// Shapes (all coordinates are math-space, not pixels):
//   point     {at:[x,y], label?, color?}
//   polygon   {vertices:[[x,y],...], labels?:[..], fill?, stroke?, closed?}
//   line      {from:[x,y], to:[x,y], label?, dashed?}
//   segment   alias of `line` (auto-extended? no — just line endpoint to endpoint)
//   circle    {center:[x,y], radius, label?, fill?, stroke?}
//   vector    {from:[x,y], to:[x,y], label?, color?}     (arrow head)
//   angle     {at:[x,y], from:[x,y], to:[x,y], label?, radius?}
//   text      {at:[x,y], text, color?}
//
// All labels go through KaTeX (`MathishText auto`).

import { useEffect, useMemo, useRef, useState } from 'react';
import { create, all } from 'mathjs';
import { MathishText } from '../lib/mathish';
import { PLOT_COLORS } from '../lib/palette';

// mathjs (function-plot 의존성으로 이미 번들에 포함). parametric expr 평가용.
const _math = create(all);
function _evalMathjs(s: string | number): number {
  if (typeof s === 'number') return s;
  try { return _math.evaluate(_normalizeMathExprStr(s)); } catch { return NaN; }
}

// 좌표 정규화 — LLM 이 'sqrt(3)'·'3*sqrt(3)' 같은 raw 수학식 string 을 좌표에
// 박는 경우 mathjs 로 evaluate. number/evaluable string → 유한 number, 아니면 null.
// (Geometry3D 의 coerceCoord/normalizeMathExprStr 와 동일한 동작.)
function _normalizeMathExprStr(s: string): string {
  return s
    .replace(/\*\*/g, '^')   // Python 거듭제곱 ** → mathjs ^ (LLM 이 t**2 쓰면 파서가 거부→곡선 소실. 결정적 보정)
    .replace(/√/g, 'sqrt').replace(/π/g, 'pi').replace(/×/g, '*').replace(/÷/g, '/').replace(/−/g, '-');
}
function _coerceCoord(v: unknown): number | null {
  if (typeof v === 'number') return Number.isFinite(v) ? v : null;
  if (typeof v === 'string') {
    const expr = _normalizeMathExprStr(v.startsWith('=') ? v.slice(1) : v);
    try {
      const r = _math.evaluate(expr);
      if (typeof r === 'number' && Number.isFinite(r)) return r;
    } catch { /* fall through */ }
    return null;
  }
  return null;
}
// [x,y] 쌍을 coerce. 둘 다 유한해야 통과, 아니면 null (해당 shape drop 신호).
function _coercePair(p: unknown): [number, number] | null {
  if (!Array.isArray(p) || p.length < 2) return null;
  const x = _coerceCoord(p[0]);
  const y = _coerceCoord(p[1]);
  return (x === null || y === null) ? null : [x, y];
}

// spec.shapes 를 정규화: 문자열/수식 좌표를 유한 number 로 강제하고, 좌표가
// 비유한(NaN/Infinity/eval 실패)인 shape 는 통째로 drop 한다. autoBounds 와
// 렌더가 같은 정규화 입력을 공유하므로, 깨진 좌표 하나가 전체 bounds 를
// 오염(±Infinity → scale=NaN → 빈 캔버스)시키는 사고를 막는다.
function normalizeShapes(shapes: GeomShape[]): GeomShape[] {
  const out: GeomShape[] = [];
  for (const s of shapes) {
    switch (s.type) {
      case 'point': {
        const at = _coercePair(s.at);
        if (at) out.push({ ...s, at });
        break;
      }
      case 'polygon': {
        const vertices = s.vertices.map((v) => _coercePair(v));
        if (vertices.every((v): v is [number, number] => v !== null)) {
          out.push({ ...s, vertices });
        }
        break;
      }
      case 'line': case 'segment': case 'vector': {
        const from = _coercePair(s.from), to = _coercePair(s.to);
        if (from && to) out.push({ ...s, from, to });
        break;
      }
      case 'circle': {
        const center = _coercePair(s.center);
        const radius = _coerceCoord(s.radius);
        if (center && radius !== null) out.push({ ...s, center, radius });
        break;
      }
      case 'ellipse': {
        const center = _coercePair(s.center);
        const rx = _coerceCoord(s.rx ?? (s as unknown as { a?: unknown }).a);
        const ry = _coerceCoord(s.ry ?? (s as unknown as { b?: unknown }).b);
        if (center && rx !== null && ry !== null) out.push({ ...s, center, rx, ry });
        break;
      }
      case 'hyperbola': {
        const center = _coercePair(s.center);
        const a = _coerceCoord(s.a), b = _coerceCoord(s.b);
        if (center && a !== null && b !== null) out.push({ ...s, center, a, b });
        break;
      }
      case 'parabola': {
        const vertex = _coercePair(s.vertex);
        const focus = s.focus === undefined ? undefined : _coerceCoord(s.focus);
        if (vertex && focus !== null) out.push({ ...s, vertex, ...(focus === undefined ? {} : { focus }) });
        break;
      }
      case 'angle': {
        const at = _coercePair(s.at), from = _coercePair(s.from), to = _coercePair(s.to);
        if (at && from && to) out.push({ ...s, at, from, to });
        break;
      }
      case 'text': {
        const at = _coercePair(s.at);
        if (at) out.push({ ...s, at });
        break;
      }
      case 'parametric':
        // 문자열 expr 좌표는 sampleParametric 가 이미 mathjs 로 평가 + 유한성 필터.
        out.push(s);
        break;
      default:
        out.push(s);
    }
  }
  return out;
}

// 매개변수 곡선을 sample. null 은 끊김 marker (NaN/Infinity/eval 실패).
function sampleParametric(
  s: { x: string; y: string; tRange: [number | string, number | string]; samples?: number },
): Array<[number, number] | null> {
  const t0 = _evalMathjs(s.tRange[0]);
  const t1 = _evalMathjs(s.tRange[1]);
  if (!Number.isFinite(t0) || !Number.isFinite(t1) || t1 <= t0) return [];
  const n = Math.max(2, Math.min(s.samples ?? 120, 2000));
  let xNode: { evaluate: (scope: { t: number }) => number };
  let yNode: { evaluate: (scope: { t: number }) => number };
  try {
    xNode = _math.parse(_normalizeMathExprStr(s.x)).compile() as typeof xNode;
    yNode = _math.parse(_normalizeMathExprStr(s.y)).compile() as typeof yNode;
  } catch {
    return [];
  }
  const out: Array<[number, number] | null> = [];
  for (let i = 0; i <= n; i++) {
    const t = t0 + ((t1 - t0) * i) / n;
    try {
      const xv = xNode.evaluate({ t });
      const yv = yNode.evaluate({ t });
      if (Number.isFinite(xv) && Number.isFinite(yv)) out.push([xv, yv]);
      else out.push(null);
    } catch {
      out.push(null);
    }
  }
  return out;
}

// area: y=f(x) 와 baseline(상수 또는 식) 사이를 [from,to] 에서 샘플.
// expr 변수는 x 또는 t 둘 다 허용(scope 에 둘 다 같은 값으로 넣음).
function sampleArea(s: {
  y: string; from: number | string; to: number | string; baseline?: number | string; samples?: number;
}): { top: Array<[number, number]>; bottom: Array<[number, number]> } {
  const x0 = _evalMathjs(s.from), x1 = _evalMathjs(s.to);
  if (!Number.isFinite(x0) || !Number.isFinite(x1) || x1 <= x0) return { top: [], bottom: [] };
  let yNode: { evaluate: (scope: { x: number; t: number }) => number };
  let bNode: { evaluate: (scope: { x: number; t: number }) => number } | null = null;
  try {
    yNode = _math.parse(_normalizeMathExprStr(s.y)).compile() as typeof yNode;
    if (typeof s.baseline === 'string') bNode = _math.parse(_normalizeMathExprStr(s.baseline)).compile() as typeof yNode;
  } catch { return { top: [], bottom: [] }; }
  const base0 = typeof s.baseline === 'number' ? s.baseline : 0;
  const n = Math.max(2, Math.min(s.samples ?? 120, 2000));
  const top: Array<[number, number]> = [], bottom: Array<[number, number]> = [];
  for (let i = 0; i <= n; i++) {
    const x = x0 + ((x1 - x0) * i) / n;
    try {
      const yv = yNode.evaluate({ x, t: x });
      const bv = bNode ? bNode.evaluate({ x, t: x }) : base0;
      if (Number.isFinite(yv) && Number.isFinite(bv)) { top.push([x, yv]); bottom.push([x, bv]); }
    } catch { /* skip */ }
  }
  return { top, bottom };
}

export type GeomShape =
  | { type: 'point'; at: [number, number]; label?: string; color?: string; labelDir?: 'NE' | 'NW' | 'SE' | 'SW' | 'N' | 'S' | 'E' | 'W' }
  | { type: 'polygon'; vertices: Array<[number, number]>; labels?: string[]; fill?: string; fillOpacity?: number; stroke?: string; closed?: boolean }
  | { type: 'line' | 'segment'; from: [number, number]; to: [number, number]; label?: string; dashed?: boolean; color?: string }
  | { type: 'circle'; center: [number, number]; radius: number; label?: string; fill?: string; fillOpacity?: number; stroke?: string }
  | { type: 'ellipse'; center: [number, number]; rx: number; ry: number; rotation?: number; label?: string; fill?: string; fillOpacity?: number; stroke?: string }
  | { type: 'hyperbola'; center: [number, number]; a: number; b: number; orientation?: 'horizontal' | 'vertical'; label?: string; color?: string }
  | { type: 'parabola'; vertex: [number, number]; focus?: number; orientation?: 'up' | 'down' | 'left' | 'right'; label?: string; color?: string }
  | { type: 'parametric'; x: string; y: string; tRange: [number | string, number | string];
      samples?: number; closed?: boolean; label?: string; color?: string;
      stroke?: string; strokeWidth?: number; fill?: string; fillOpacity?: number }
  | { type: 'vector'; from: [number, number]; to: [number, number]; label?: string; color?: string }
  | { type: 'angle'; at: [number, number]; from: [number, number]; to: [number, number]; label?: string; radius?: number; color?: string }
  | { type: 'text'; at: [number, number]; text: string; color?: string }
  | { type: 'area'; y: string; from: number | string; to: number | string;
      baseline?: number | string; samples?: number; fill?: string; fillOpacity?: number; stroke?: string; label?: string };

export type GeomSpec = {
  shapes: GeomShape[];
  range?: [number, number];
  yRange?: [number, number];
  showAxes?: boolean;
  showGrid?: boolean;
  title?: string;
  width?: number;
  height?: number;
};

// Geometry labels render as LaTeX by default — use the shared MathishText
// in `auto` mode so bare strings like "x^2" are treated as math.
const GeomLabel = ({ text }: { text: string }) => <MathishText text={text} auto />;

// Default to a square-ish frame so geometry stays undistorted.
const DEFAULT_WIDTH = 380;
const DEFAULT_HEIGHT = 320;

function fmtNum(n: number): string {
  if (!Number.isFinite(n)) return '?';
  const s = Math.abs(n) >= 100 ? n.toFixed(0) : n.toFixed(2);
  return s.includes('.') ? s.replace(/\.?0+$/, '') : s;
}

// Auto-fit a spec's bounding box so geometry comfortably fills the canvas.
function autoBounds(shapes: GeomShape[]): { x: [number, number]; y: [number, number] } {
  const xs: number[] = [], ys: number[] = [];
  for (const s of shapes) {
    switch (s.type) {
      case 'point':  xs.push(s.at[0]); ys.push(s.at[1]); break;
      case 'polygon': for (const v of s.vertices) { xs.push(v[0]); ys.push(v[1]); } break;
      case 'line': case 'segment': case 'vector':
        xs.push(s.from[0], s.to[0]); ys.push(s.from[1], s.to[1]); break;
      case 'circle':
        xs.push(s.center[0] - s.radius, s.center[0] + s.radius);
        ys.push(s.center[1] - s.radius, s.center[1] + s.radius);
        break;
      case 'ellipse': {
        const rx = (s.rx ?? (s as unknown as { a?: number }).a) as number;
        const ry = (s.ry ?? (s as unknown as { b?: number }).b) as number;
        if (typeof rx !== 'number' || typeof ry !== 'number') break;
        xs.push(s.center[0] - rx, s.center[0] + rx);
        ys.push(s.center[1] - ry, s.center[1] + ry);
        break;
      }
      case 'hyperbola': {
        // 점근선 비율에 따라 적당히 시각 범위
        const span = Math.max(s.a, s.b) * 3;
        xs.push(s.center[0] - span, s.center[0] + span);
        ys.push(s.center[1] - span, s.center[1] + span);
        break;
      }
      case 'parabola': {
        const span = (s.focus ?? 1) * 4;
        xs.push(s.vertex[0] - span, s.vertex[0] + span);
        ys.push(s.vertex[1] - span, s.vertex[1] + span);
        break;
      }
      case 'parametric': {
        // 실제 sample 한 점들을 bbox 에 포함.
        for (const pt of sampleParametric(s)) {
          if (pt) { xs.push(pt[0]); ys.push(pt[1]); }
        }
        break;
      }
      case 'area': {
        const { top, bottom } = sampleArea(s);
        for (const p of top) { xs.push(p[0]); ys.push(p[1]); }
        for (const p of bottom) { ys.push(p[1]); }
        break;
      }
      case 'angle':
        xs.push(s.at[0], s.from[0], s.to[0]); ys.push(s.at[1], s.from[1], s.to[1]); break;
      case 'text':
        xs.push(s.at[0]); ys.push(s.at[1]); break;
    }
  }
  // 비유한 좌표(±Infinity from JSON.parse('1e309'), NaN)는 제외 — 단 하나라도
  // 섞이면 min/max 가 ±Infinity 가 되어 padX=Infinity → scale=NaN → 빈 캔버스.
  const fxs = xs.filter(Number.isFinite), fys = ys.filter(Number.isFinite);
  if (fxs.length === 0 || fys.length === 0) return { x: [-5, 5], y: [-5, 5] };
  const xMin = Math.min(...fxs), xMax = Math.max(...fxs);
  const yMin = Math.min(...fys), yMax = Math.max(...fys);
  // padding 15% — 점이 viewport 끝에 안 붙도록. (25%→15%: 도형이 너무 작게 렌더돼
  // 내부 라벨이 비좁던 문제 완화 — 그림을 키워 라벨이 퍼질 공간 확보.) min 0.4.
  const padX = Math.max((xMax - xMin) * 0.15, 0.4);
  const padY = Math.max((yMax - yMin) * 0.15, 0.4);
  return { x: [xMin - padX, xMax + padX], y: [yMin - padY, yMax + padY] };
}

function GeometryCanvas({ spec, width, height, hideCaption = false, fixedWidth }: { spec: GeomSpec; width: number; height: number; hideCaption?: boolean; fixedWidth?: number }) {
  const wrapRef = useRef<HTMLDivElement | null>(null);
  // fixedWidth: ResizeObserver 우회 → 부모폭 측정 없이 그 폭으로 고정 렌더.
  // 헤드리스 스크린샷이 부모 clientWidth 를 과소측정(240 floor)해 실제보다 작게/라벨이
  // 뭉쳐 보이던 문제를 우회 — QA 시각 검수용 결정적 실측 렌더.
  const [effWidth, setEffWidth] = useState(fixedWidth ?? width);
  // 라벨 드래그: 키별 픽셀 offset. 움직인 라벨엔 home→현재 leader 선을 그린다(안 움직이면 숨김).
  const [labelDrag, setLabelDrag] = useState<Record<string, { dx: number; dy: number }>>({});
  const dragRef = useRef<{ key: string; sx: number; sy: number; bdx: number; bdy: number } | null>(null);
  // spec 바뀌면 드래그 초기화(라벨 키가 새 도식과 충돌하지 않도록).
  useEffect(() => { setLabelDrag({}); }, [spec]);

  useEffect(() => {
    if (fixedWidth) return;   // 고정폭이면 측정 안 함
    const el = wrapRef.current;
    if (!el) return;
    // ★ client:load 로 단독 마운트되면 부모가 <astro-island>(display:contents, clientWidth=0)라
    // el.parentElement.clientWidth 가 0 → 240 floor 로 고정되던 버그. display:contents/0폭 래퍼를
    // 건너뛰고 **실제 레이아웃 폭을 가진 첫 조상**을 측정·관측한다. (ChatPanel 내부 자식일 땐
    // 부모가 일반 박스라 그대로 동작.)
    const layoutBox = (): HTMLElement | null => {
      let n: HTMLElement | null = el.parentElement;
      while (n && n.clientWidth === 0) n = n.parentElement;
      return n;
    };
    // rAF-throttle + ≥1px change guard — prevents ResizeObserver feedback
    // loops from pegging the main thread (see Graph.tsx PlotGraph for detail).
    let raf = 0;
    const measure = () => {
      raf = 0;
      const pw = layoutBox()?.clientWidth ?? width;
      const target = Math.round(Math.min(width, Math.max(240, pw - 16)));
      setEffWidth((prev) => (Math.abs(prev - target) < 1 ? prev : target));
    };
    measure();
    const box = layoutBox();
    const ro = new ResizeObserver(() => { if (!raf) raf = requestAnimationFrame(measure); });
    if (box) ro.observe(box);
    return () => { if (raf) cancelAnimationFrame(raf); ro.disconnect(); };
  }, [width, fixedWidth]);

  // 문자열/수식 좌표를 유한 number 로 강제하고, 깨진 좌표 shape 는 drop.
  // autoBounds·렌더가 같은 정규화 입력을 쓰도록 한 번만 계산.
  const shapes = useMemo(() => normalizeShapes(spec.shapes), [spec.shapes]);

  const bounds = useMemo(() => {
    const auto = autoBounds(shapes);
    // LLM 명시 range/yRange 가 auto 보다 작으면 union — 모든 점이 화면 안 보장.
    // 명시 안 했으면 auto 사용.
    const ux: [number, number] = spec.range
      ? [Math.min(spec.range[0], auto.x[0]), Math.max(spec.range[1], auto.x[1])]
      : auto.x;
    const uy: [number, number] = spec.yRange
      ? [Math.min(spec.yRange[0], auto.y[0]), Math.max(spec.yRange[1], auto.y[1])]
      : auto.y;
    return { x: ux, y: uy };
  }, [shapes, spec.range, spec.yRange]);

  // Map math coords → pixel coords, equal-aspect scaling so shapes
  // don't get distorted.
  const PAD = 24;
  const xSpan = bounds.x[1] - bounds.x[0];
  const ySpan = bounds.y[1] - bounds.y[0];
  // 요청 W×H 안에서 등비 최대 스케일을 잡되, 캔버스를 콘텐츠 크기로 *크롭*한다.
  // (이전: 캔버스를 요청 W×H 로 두고 콘텐츠를 가운데 정렬 → 정사각 도형이 가로로 긴
  //  캔버스 안에서 작아 보이고 가로 여백만 남았다. 이제 도형이 캔버스를 꽉 채운다.)
  const scale = Math.min((effWidth - 2 * PAD) / xSpan, (height - 2 * PAD) / ySpan);
  const contentW = scale * xSpan, contentH = scale * ySpan;
  // 세로로 긴 도식(콘텐츠 높이 ≫ 폭)은 캔버스가 좁아 라벨이 가장자리에 몰린다.
  // 그런 경우 좌우에 라벨 공간용 패딩을 추가(레이아웃에 남는 가로 여백 활용). 폭은 effWidth 안에서.
  const tall = contentH > contentW * 1.4;
  const extraX = tall
    ? Math.round(Math.min((contentH - contentW) * 0.25, contentW * 0.6, Math.max(0, (effWidth - contentW) / 2 - PAD)))
    : 0;
  const padXSide = PAD + extraX;
  const W = Math.round(contentW + 2 * padXSide);
  const H = Math.round(contentH + 2 * PAD);
  const cx = padXSide, cy = PAD;
  const xPx = (x: number) => cx + (x - bounds.x[0]) * scale;
  const yPx = (y: number) => H - cy - (y - bounds.y[0]) * scale;

  const showAxes = spec.showAxes !== false;
  const showGrid = spec.showGrid !== false;

  // Choose tick step
  const tickStep = (() => {
    const s = Math.max(xSpan, ySpan);
    const target = s / 10;
    for (const c of [0.1, 0.2, 0.25, 0.5, 1, 2, 5, 10, 20, 50]) if (c >= target) return c;
    return 100;
  })();

  // Scale overlay-label font with canvas width — labels grow with the
  // panel up to a cap so they stay legible without dominating the figure.
  // axis-tick font is one step smaller than the math labels.
  const labelFontPx = Math.max(11, Math.min(18, Math.round(effWidth / 40)));
  const tickFontPx = Math.max(9, labelFontPx - 2);

  // Build SVG elements ----------------------------------------------------
  const els: React.ReactNode[] = [];
  // 라벨은 디스크립터로 모은 뒤(좌표·정렬 기준점) 충돌 회피(de-overlap)를 거쳐 렌더.
  // tx: translateX(%) — 0=좌측정렬, -50=중앙, -100=우측정렬(앵커가 라벨 우상단).
  // anchor: 라벨이 가리키는 실제 도형 지점(픽셀). 드래그 시 leader 선이 여기로 향한다.
  // 미지정 시 라벨 자기 위치([left,top]) — 곡선/중심 라벨처럼 도형에 붙은 경우.
  type LabelDesc = { key: string; text: string; left: number; top: number; tx: number; color?: string; fixed?: boolean; anchor: [number, number] };
  const labelDescs: LabelDesc[] = [];
  // fixed=true: 위치 의미가 고정인 라벨(각 θ 는 각 안에 있어야 의미) — de-overlap 에 안 밀린다(다른 라벨이 이걸 피함).
  const pushLabel = (key: string, text: string, left: number, top: number, tx = 0, color?: string, fixed = false, anchor?: [number, number]) =>
    labelDescs.push({ key, text, left, top, tx, color, fixed, anchor: anchor ?? [left, top] });
  // 도형 외곽선(픽셀 세그먼트) — 라벨이 선·원·다각형을 가리지 않게 밀어낼 장애물.
  const obstacles: Array<[number, number, number, number]> = [];
  const addSeg = (x1: number, y1: number, x2: number, y2: number) => obstacles.push([x1, y1, x2, y2]);
  const addCircleObstacle = (cxp: number, cyp: number, rp: number) => {
    const N = 28;
    for (let k = 0; k < N; k++) {
      const a1 = (2 * Math.PI * k) / N, a2 = (2 * Math.PI * (k + 1)) / N;
      addSeg(cxp + rp * Math.cos(a1), cyp + rp * Math.sin(a1), cxp + rp * Math.cos(a2), cyp + rp * Math.sin(a2));
    }
  };
  // 도형 중심(px) — 선 라벨을 선의 '바깥쪽'(중심 반대편)에 두기 위함.
  let _csx = 0, _csy = 0, _csn = 0;
  for (const s of shapes) {
    const ps: Array<[number, number]> = [];
    if (s.type === 'point') ps.push(s.at);
    else if (s.type === 'polygon') ps.push(...s.vertices);
    else if (s.type === 'line' || s.type === 'segment' || s.type === 'vector') ps.push(s.from, s.to);
    else if (s.type === 'circle' || s.type === 'ellipse' || s.type === 'hyperbola') ps.push(s.center);
    else if (s.type === 'angle') ps.push(s.at);
    for (const p of ps) if (typeof p?.[0] === 'number' && typeof p?.[1] === 'number') { _csx += p[0]; _csy += p[1]; _csn++; }
  }
  const ctrX = _csn ? _csx / _csn : (bounds.x[0] + bounds.x[1]) / 2;
  const ctrY = _csn ? _csy / _csn : (bounds.y[0] + bounds.y[1]) / 2;
  const ctrPx: [number, number] = [xPx(ctrX), yPx(ctrY)];
  // 선분 중점에서 선의 수직 바깥쪽(중심 반대)으로 라벨 위치 계산.
  const outwardLabel = (ax: number, ay: number, bx: number, by: number, off: number): [number, number] => {
    const mx = (xPx(ax) + xPx(bx)) / 2, my = (yPx(ay) + yPx(by)) / 2;
    let nx = -(yPx(by) - yPx(ay)), ny = (xPx(bx) - xPx(ax));
    const nl = Math.hypot(nx, ny) || 1; nx /= nl; ny /= nl;
    if ((mx - ctrPx[0]) * nx + (my - ctrPx[1]) * ny < 0) { nx = -nx; ny = -ny; }
    return [mx + nx * off, my + ny * off];
  };
  // 꼭짓점(vx,vy 데이터좌표) 라벨을 도형 '바깥쪽'(기준중심 cx,cy 반대 방향)으로 off(px) 띄운다.
  // 다각형 꼭짓점 라벨이 도형 내부에 들어가는 것 방지. tx 는 좌/우/중앙 정렬.
  const outwardFromCenter = (vx: number, vy: number, cx: number, cy: number, off: number): [number, number, number] => {
    let dx = xPx(vx) - xPx(cx), dy = yPx(vy) - yPx(cy);
    const dl = Math.hypot(dx, dy) || 1; dx /= dl; dy /= dl;
    const tx = dx < -0.35 ? -100 : (dx > 0.35 ? 0 : -50);
    return [xPx(vx) + dx * off, yPx(vy) + dy * off, tx];
  };

  // Grid
  if (showGrid) {
    const minX = Math.ceil(bounds.x[0] / tickStep) * tickStep;
    const maxX = bounds.x[1];
    for (let v = minX; v <= maxX + 1e-9; v += tickStep) {
      els.push(<line key={`gx${v}`} x1={xPx(v)} y1={yPx(bounds.y[0])} x2={xPx(v)} y2={yPx(bounds.y[1])}
                     stroke="#3f3f46" strokeWidth={0.5} opacity={0.6} />);
    }
    const minY = Math.ceil(bounds.y[0] / tickStep) * tickStep;
    const maxY = bounds.y[1];
    for (let v = minY; v <= maxY + 1e-9; v += tickStep) {
      els.push(<line key={`gy${v}`} x1={xPx(bounds.x[0])} y1={yPx(v)} x2={xPx(bounds.x[1])} y2={yPx(v)}
                     stroke="#3f3f46" strokeWidth={0.5} opacity={0.6} />);
    }
  }

  // Axes (only draw if origin is inside visible domain)
  if (showAxes) {
    if (bounds.y[0] <= 0 && bounds.y[1] >= 0) {
      els.push(<line key="xax" x1={xPx(bounds.x[0])} y1={yPx(0)} x2={xPx(bounds.x[1])} y2={yPx(0)}
                     stroke="#fafafa" strokeWidth={1.4} />);
    }
    if (bounds.x[0] <= 0 && bounds.x[1] >= 0) {
      els.push(<line key="yax" x1={xPx(0)} y1={yPx(bounds.y[0])} x2={xPx(0)} y2={yPx(bounds.y[1])}
                     stroke="#fafafa" strokeWidth={1.4} />);
    }
    // Tick labels along the bottom + left edges
    const minX = Math.ceil(bounds.x[0] / tickStep) * tickStep;
    for (let v = minX; v <= bounds.x[1] + 1e-9; v += tickStep) {
      if (Math.abs(v) < 1e-9) continue;
      els.push(<text key={`tx${v}`} x={xPx(v)} y={H - 6} fill="#a1a1aa" fontSize={tickFontPx} textAnchor="middle">{fmtNum(v)}</text>);
    }
    const minY = Math.ceil(bounds.y[0] / tickStep) * tickStep;
    for (let v = minY; v <= bounds.y[1] + 1e-9; v += tickStep) {
      if (Math.abs(v) < 1e-9) continue;
      els.push(<text key={`ty${v}`} x={4} y={yPx(v) + 4} fill="#a1a1aa" fontSize={tickFontPx}>{fmtNum(v)}</text>);
    }
  }

  // 같은 (좌표, 라벨) 페어의 중복 라벨 dedup 용. LLM 이 종종 한 점에 대해
  // point shape + polygon vertex labels 양쪽으로 같은 라벨을 emit 해서
  // 같은 문자가 두 번 그려지는 사고를 막는다.
  const claimedLabels = new Set<string>();
  for (const s of shapes) {
    if (s.type === 'point' && s.label
        && Array.isArray(s.at) && typeof s.at[0] === 'number' && typeof s.at[1] === 'number'
        && Number.isFinite(s.at[0]) && Number.isFinite(s.at[1])) {
      claimedLabels.add(`${s.at[0].toFixed(2)},${s.at[1].toFixed(2)}|${s.label}`);
    }
  }

  // Shapes
  shapes.forEach((s, i) => {
    const c0 = PLOT_COLORS[i % PLOT_COLORS.length];
    switch (s.type) {
      case 'point': {
        const [x, y] = s.at;
        els.push(<circle key={`pt${i}`} cx={xPx(x)} cy={yPx(y)} r={4} fill={s.color ?? '#fb7185'}
                         stroke="#fafafa" strokeWidth={1.5} />);
        if (s.label) {
          // labelDir: NE(default) / NW / SE / SW / N / S / E / W
          // 각 방향마다 점에서 라벨 좌상단까지 offset 계산. label 폭 추정 X →
          // W/SW/NW 방향은 transform translateX(-100%) 로 우측 정렬.
          const dir = s.labelDir ?? 'NE';
          // 라벨을 점에 바짝 붙인다(좌표에서 멀어지면 무엇을 가리키는지 안 보임).
          // 점 반지름(4) + 약간의 여백만 띄운다.
          const offX = (() => {
            if (dir.includes('E')) return 7;
            if (dir.includes('W')) return -7;
            return 0;
          })();
          const offY = (() => {
            if (dir.includes('N')) return -labelFontPx - 3;
            if (dir.includes('S')) return 7;
            return -labelFontPx / 2 - 2;
          })();
          const tx = dir.includes('W') ? -100 : (dir.includes('E') ? 0 : -50);
          pushLabel(`pl${i}`, s.label, xPx(x) + offX, yPx(y) + offY, tx, undefined, false, [xPx(x), yPx(y)]);
        }
        break;
      }
      case 'polygon': {
        const pts = s.vertices.map((v) => `${xPx(v[0])},${yPx(v[1])}`).join(' ');
        const closed = s.closed !== false;
        // fillOpacity default 0.18 — 안쪽 도형/라벨 가리지 않게.
        // LLM 이 명시한 fill 색이 hex 같이 알파 정보 없는 형식이면 fillOpacity 적용.
        const fillCol = s.fill ?? `${c0}33`;
        const fillOp = s.fillOpacity ?? 0.18;
        els.push(closed
          ? <polygon key={`pg${i}`} points={pts} fill={fillCol} fillOpacity={fillOp} stroke={s.stroke ?? c0} strokeWidth={1.8} />
          : <polyline key={`pg${i}`} points={pts} fill="none" stroke={s.stroke ?? c0} strokeWidth={1.8} />);
        for (let vi = 0; vi < s.vertices.length - (closed ? 0 : 1); vi++) {
          const p1 = s.vertices[vi], p2 = s.vertices[(vi + 1) % s.vertices.length];
          if (p1 && p2) addSeg(xPx(p1[0]), yPx(p1[1]), xPx(p2[0]), yPx(p2[1]));
        }
        if (s.labels) {
          // 이 다각형 자신의 무게중심 — 꼭짓점 라벨을 그 반대(=도형 바깥)로 밀어낸다.
          let pcx = 0, pcy = 0, pcn = 0;
          for (const v of s.vertices) {
            if (typeof v?.[0] === 'number' && typeof v?.[1] === 'number') { pcx += v[0]; pcy += v[1]; pcn++; }
          }
          pcx = pcn ? pcx / pcn : 0; pcy = pcn ? pcy / pcn : 0;
          s.labels.forEach((lab, vi) => {
            const v = s.vertices[vi]; if (!v) return;
            if (typeof v[0] !== 'number' || typeof v[1] !== 'number') return;
            // 같은 (좌표, 라벨) 의 point shape 이 이미 라벨 그렸으면 skip — 중복 방지
            const key = `${v[0].toFixed(2)},${v[1].toFixed(2)}|${lab}`;
            if (claimedLabels.has(key)) return;
            claimedLabels.add(key);
            const [lax, lay, ltx] = outwardFromCenter(v[0], v[1], pcx, pcy, labelFontPx * 0.45 + 5);
            pushLabel(`pgl${i}_${vi}`, lab, lax, lay - labelFontPx * 0.7, ltx, undefined, false, [xPx(v[0]), yPx(v[1])]);
            els.push(<circle key={`pgv${i}_${vi}`} cx={xPx(v[0])} cy={yPx(v[1])} r={3} fill="#fafafa" />);
          });
        }
        break;
      }
      case 'line': case 'segment': {
        els.push(<line key={`ln${i}`} x1={xPx(s.from[0])} y1={yPx(s.from[1])} x2={xPx(s.to[0])} y2={yPx(s.to[1])}
                       stroke={s.color ?? c0} strokeWidth={1.8} strokeDasharray={s.dashed ? '6 4' : undefined} />);
        addSeg(xPx(s.from[0]), yPx(s.from[1]), xPx(s.to[0]), yPx(s.to[1]));
        if (s.label) {
          const [llx, lly] = outwardLabel(s.from[0], s.from[1], s.to[0], s.to[1], labelFontPx * 0.95 + 6);
          pushLabel(`lnl${i}`, s.label, llx, lly - labelFontPx * 0.7, -50); // top→세로 중앙정렬
        }
        break;
      }
      case 'circle': {
        // r 은 절댓값 — 부호 있는 계산값으로 음수 radius 가 넘어오면 SVG <circle>
        // 사양상 r<0 은 무효라 원이 에러 없이 사라진다(autoBounds 는 ±radius 라 생존).
        els.push(<circle key={`ci${i}`} cx={xPx(s.center[0])} cy={yPx(s.center[1])} r={Math.abs(s.radius) * scale}
                         fill={s.fill ?? 'none'} fillOpacity={s.fillOpacity ?? (s.fill ? 0.18 : 1)}
                         stroke={s.stroke ?? c0} strokeWidth={1.8} />);
        addCircleObstacle(xPx(s.center[0]), yPx(s.center[1]), Math.abs(s.radius) * scale);
        if (s.label) pushLabel(`cil${i}`, s.label, xPx(s.center[0]) + 4, yPx(s.center[1]) - 6);
        break;
      }
      case 'ellipse': {
        // SVG ellipse — rx*scale, ry*scale (y축 scale 같다고 가정). rotation은 deg.
        // LLM 이 a/b 키로 박는 케이스 대비 — fallback alias.
        const rxRaw = (s.rx ?? (s as unknown as { a?: number }).a) as number;
        const ryRaw = (s.ry ?? (s as unknown as { b?: number }).b) as number;
        if (typeof rxRaw !== 'number' || typeof ryRaw !== 'number') break;
        const cx = xPx(s.center[0]), cy = yPx(s.center[1]);
        const rxPx = rxRaw * scale, ryPx = ryRaw * scale;
        const transform = s.rotation ? `rotate(${-s.rotation} ${cx} ${cy})` : undefined;
        els.push(<ellipse key={`el${i}`} cx={cx} cy={cy} rx={rxPx} ry={ryPx}
                          fill={s.fill ?? 'none'} fillOpacity={s.fillOpacity ?? (s.fill ? 0.18 : 1)}
                          stroke={s.stroke ?? c0} strokeWidth={1.8}
                          transform={transform} />);
        if (s.label) pushLabel(`ell${i}`, s.label, xPx(s.center[0]) + 4, yPx(s.center[1] + ryRaw) + 4);
        break;
      }
      case 'hyperbola': {
        // x²/a² − y²/b² = 1 (horizontal) 또는 y²/a² − x²/b² = 1 (vertical)
        // 두 가지 (좌·우 또는 상·하) curve 를 polyline 으로 샘플링.
        const horiz = (s.orientation ?? 'horizontal') === 'horizontal';
        const a = s.a, b = s.b;
        const cx0 = s.center[0], cy0 = s.center[1];
        const samples = 80;
        const tMax = 2;
        const pts1: string[] = [], pts2: string[] = [];
        for (let k = 0; k <= samples; k++) {
          const t = -tMax + (2 * tMax * k) / samples;
          if (horiz) {
            const x = a * Math.cosh(t);
            const y = b * Math.sinh(t);
            pts1.push(`${xPx(cx0 + x)},${yPx(cy0 + y)}`);
            pts2.push(`${xPx(cx0 - x)},${yPx(cy0 + y)}`);
          } else {
            const x = b * Math.sinh(t);
            const y = a * Math.cosh(t);
            pts1.push(`${xPx(cx0 + x)},${yPx(cy0 + y)}`);
            pts2.push(`${xPx(cx0 + x)},${yPx(cy0 - y)}`);
          }
        }
        els.push(<polyline key={`hy1${i}`} points={pts1.join(' ')} fill="none"
                            stroke={s.color ?? c0} strokeWidth={1.8} />);
        els.push(<polyline key={`hy2${i}`} points={pts2.join(' ')} fill="none"
                            stroke={s.color ?? c0} strokeWidth={1.8} />);
        if (s.label) pushLabel(`hyl${i}`, s.label, xPx(cx0) + 4, yPx(cy0) + 8);
        break;
      }
      case 'parabola': {
        // (x - h)² = 4p (y - k) [up/down] / (y - k)² = 4p (x - h) [left/right]
        const o = s.orientation ?? 'up';
        const [h, k] = s.vertex;
        const p = s.focus ?? 1;
        const samples = 80;
        const span = Math.abs(p) * 4;
        const pts: string[] = [];
        for (let i2 = 0; i2 <= samples; i2++) {
          const t = -span + (2 * span * i2) / samples;
          let x = h, y = k;
          if (o === 'up')        { x = h + t; y = k + (t * t) / (4 * p); }
          else if (o === 'down') { x = h + t; y = k - (t * t) / (4 * p); }
          else if (o === 'right'){ y = k + t; x = h + (t * t) / (4 * p); }
          else if (o === 'left') { y = k + t; x = h - (t * t) / (4 * p); }
          pts.push(`${xPx(x)},${yPx(y)}`);
        }
        els.push(<polyline key={`pa${i}`} points={pts.join(' ')} fill="none"
                            stroke={s.color ?? c0} strokeWidth={1.8} />);
        if (s.label) pushLabel(`pal${i}`, s.label, xPx(h) + 4, yPx(k) - 12);
        break;
      }
      case 'area': {
        // 곡선 y=f(x) 와 baseline(기본 0) 사이 영역을 반투명 채움 — 적분·넓이·부호영역 시각화.
        // (선 다발로 영역을 흉내내지 말 것: area 한 개로 면을 채운다.)
        const { top, bottom } = sampleArea(s);
        if (top.length >= 2) {
          const fwd = top.map((p) => `${xPx(p[0])},${yPx(p[1])}`);
          const back = bottom.slice().reverse().map((p) => `${xPx(p[0])},${yPx(p[1])}`);
          const d = `M${fwd[0]} L${fwd.slice(1).join(' L')} L${back.join(' L')} Z`;
          els.push(
            <path key={`area${i}`} d={d}
                  fill={s.fill ?? '#6366f1'} fillOpacity={s.fillOpacity ?? 0.22}
                  stroke={s.stroke ?? 'none'} strokeWidth={s.stroke ? 1.5 : 0} />,
          );
          if (s.label) {
            const m = Math.floor(top.length / 2);
            pushLabel(`areal${i}`, s.label, xPx(top[m][0]), yPx((top[m][1] + bottom[m][1]) / 2));
          }
        }
        break;
      }
      case 'parametric': {
        // 어떤 매개변수 곡선이든 sample → polyline (closed=true 면 polygon).
        // null 은 끊김 marker — polyline 을 그 자리에서 잘라 새로 시작.
        const samples = sampleParametric(s);
        const segments: string[][] = [[]];
        for (const pt of samples) {
          if (pt) {
            segments[segments.length - 1].push(`${xPx(pt[0])},${yPx(pt[1])}`);
          } else if (segments[segments.length - 1].length > 0) {
            segments.push([]);
          }
        }
        const strokeColor = s.stroke ?? s.color ?? c0;
        const sw = s.strokeWidth ?? 1.8;
        for (let si = 0; si < segments.length; si++) {
          const seg = segments[si];
          if (seg.length < 2) continue;
          if (s.closed && si === 0 && s.fill) {
            // 첫 segment + closed → polygon (fill 포함). 끊긴 segment 는 fill X.
            els.push(
              <polygon key={`pmF${i}-${si}`} points={seg.join(' ')}
                       fill={s.fill} fillOpacity={s.fillOpacity ?? 0.18}
                       stroke={strokeColor} strokeWidth={sw} />,
            );
          } else {
            els.push(
              <polyline key={`pm${i}-${si}`} points={seg.join(' ')}
                        fill="none" stroke={strokeColor} strokeWidth={sw} />,
            );
          }
        }
        // label: 첫 segment 의 중간 sample 부근
        if (s.label && segments[0].length > 0) {
          const mid = segments[0][Math.floor(segments[0].length / 2)];
          const [mx, my] = mid.split(',').map(Number);
          pushLabel(`pml${i}`, s.label, mx + 4, my - 12);
        }
        break;
      }
      case 'vector': {
        const arrowId = `arrow-${i}`;
        els.push(
          <g key={`vec${i}`}>
            <defs>
              <marker id={arrowId} viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 0 L 10 5 L 0 10 z" fill={s.color ?? c0} />
              </marker>
            </defs>
            <line x1={xPx(s.from[0])} y1={yPx(s.from[1])} x2={xPx(s.to[0])} y2={yPx(s.to[1])}
                  stroke={s.color ?? c0} strokeWidth={2} markerEnd={`url(#${arrowId})`} />
          </g>
        );
        addSeg(xPx(s.from[0]), yPx(s.from[1]), xPx(s.to[0]), yPx(s.to[1]));
        if (s.label) {
          const [vlx, vly] = outwardLabel(s.from[0], s.from[1], s.to[0], s.to[1], labelFontPx * 0.95 + 6);
          pushLabel(`vecl${i}`, s.label, vlx, vly - labelFontPx * 0.7, -50);
        }
        break;
      }
      case 'angle': {
        const r = s.radius ?? 0.5;
        const rPx = r * scale;
        const cx = xPx(s.at[0]), cy = yPx(s.at[1]);
        // ★호는 **픽셀 좌표**에서 계산한다(math 좌표는 y 가 위, SVG 는 y 가 아래라
        // 부호가 뒤집혀 large-arc-flag 가 반대로 잡혀 *외각(반사각)* 이 그려지던 버그).
        // 두 팔 사이의 **작은 각(=내각, ≤180°)** 호만 그린다: large-arc-flag=0 고정,
        // sweep-flag 는 픽셀공간 부호각으로 방향만 결정.
        const pa1 = Math.atan2(yPx(s.from[1]) - cy, xPx(s.from[0]) - cx);
        const pa2 = Math.atan2(yPx(s.to[1]) - cy, xPx(s.to[0]) - cx);
        let d = pa2 - pa1;
        while (d > Math.PI) d -= 2 * Math.PI;
        while (d <= -Math.PI) d += 2 * Math.PI;       // (-π, π] — 최소각, 부호=회전방향
        const u1x = Math.cos(pa1), u1y = Math.sin(pa1);
        const u2x = Math.cos(pa2), u2y = Math.sin(pa2);
        // ★직각(두 팔이 수직)은 호가 아니라 **작은 정사각형 마커**로 그린다(교과서 표기).
        const isRight = Math.abs(Math.abs(d) - Math.PI / 2) < 0.06;   // ~3.4° 이내
        // 라벨이 순수 각도값(90°/직각)이면 마커가 대신하므로 생략.
        const labelIsDegree = s.label != null && /^\s*(\d{1,3}\s*°?|직각|right)\s*$/i.test(String(s.label));
        if (isRight) {
          const m = Math.max(8, Math.min(rPx, 16));   // 직각 표식 정사각형 한 변(px)
          const sq = `M ${cx + u1x * m} ${cy + u1y * m} L ${cx + (u1x + u2x) * m} ${cy + (u1y + u2y) * m} L ${cx + u2x * m} ${cy + u2y * m}`;
          els.push(<path key={`ag${i}`} d={sq} fill="none" stroke={s.color ?? c0} strokeWidth={1.5} />);
          if (s.label && !labelIsDegree) {
            const midPa = pa1 + d / 2;
            const lr = m * 1.7 + labelFontPx * 0.4;
            pushLabel(`agl${i}`, s.label, cx + lr * Math.cos(midPa), cy + lr * Math.sin(midPa) - labelFontPx * 0.7, -50, undefined, true);
          }
        } else {
          const sx = cx + rPx * u1x, sy = cy + rPx * u1y;
          const ex = cx + rPx * u2x, ey = cy + rPx * u2y;
          const sweepFlag = d > 0 ? 1 : 0;              // SVG(y-down): 양의각방향=sweep 1
          const dPath = `M ${sx} ${sy} A ${rPx} ${rPx} 0 0 ${sweepFlag} ${ex} ${ey}`;
          els.push(<path key={`ag${i}`} d={dPath} fill="none" stroke={s.color ?? c0} strokeWidth={1.5} />);
          if (s.label) {
            // 라벨은 호 중앙(이등분선=pa1+d/2) 방향, 호 바깥쪽으로 살짝. 픽셀공간에서 직접.
            const midPa = pa1 + d / 2;
            const lr = rPx * 1.35 + labelFontPx * 0.4;
            pushLabel(`agl${i}`, s.label, cx + lr * Math.cos(midPa), cy + lr * Math.sin(midPa) - labelFontPx * 0.7, -50, undefined, true);
          }
        }
        break;
      }
      case 'text': {
        pushLabel(`tx${i}`, s.text, xPx(s.at[0]) + 4, yPx(s.at[1]) - 8, 0, s.color);
        break;
      }
    }
  });

  // 라벨 충돌 회피 — 가까운 앵커의 라벨끼리 겹치던 것(단위원 1·θ·sin·cos 등) 분리.
  const resolvedLabels = deOverlapLabels(labelDescs, labelFontPx, W, H, obstacles);

  return (
    <div ref={wrapRef} className="graph-host bg-zinc-950 border border-zinc-700/80 rounded-lg shadow-inner max-w-full"
         style={{ padding: '10px 12px', ['--geom-label-size' as string]: `${labelFontPx}px` } as React.CSSProperties}>
      {!hideCaption && spec.title && (
        <div className="text-zinc-300 mb-1 px-1 break-keep" style={{ fontSize: labelFontPx + 1 }}>
          <GeomLabel text={spec.title} />
        </div>
      )}
      <div style={{ position: 'relative', width: W, height: H, overflow: 'hidden' }}>
        <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} className="graph-svg"
             style={{ display: 'block', overflow: 'hidden' }}
             preserveAspectRatio="xMidYMid meet">
          {els}
          {/* 드래그된 라벨 → 원래 위치(가리키는 지점) leader 선. 안 움직였으면 안 그림. */}
          {resolvedLabels.map((d) => {
            const o = labelDrag[d.key];
            if (!o || (o.dx === 0 && o.dy === 0)) return null;
            // leader: 실제 도형 앵커 → 드래그된 라벨 위치.
            return <line key={`ld${d.key}`} x1={d.anchor[0]} y1={d.anchor[1]} x2={d.left + o.dx} y2={d.top + o.dy}
                         stroke="#9ca3af" strokeWidth={1} strokeDasharray="2 2" pointerEvents="none" />;
          })}
        </svg>
        {resolvedLabels.map((d) => {
          const o = labelDrag[d.key];
          return (
            <div key={d.key} className="geom-label"
                 onPointerDown={(e) => {
                   e.stopPropagation();
                   (e.currentTarget as HTMLElement).setPointerCapture?.(e.pointerId);
                   dragRef.current = { key: d.key, sx: e.clientX, sy: e.clientY, bdx: o?.dx ?? 0, bdy: o?.dy ?? 0 };
                 }}
                 onPointerMove={(e) => {
                   const dr = dragRef.current;
                   if (!dr || dr.key !== d.key) return;
                   setLabelDrag((m) => ({ ...m, [d.key]: { dx: dr.bdx + (e.clientX - dr.sx), dy: dr.bdy + (e.clientY - dr.sy) } }));
                 }}
                 onPointerUp={(e) => { e.stopPropagation(); if (dragRef.current?.key === d.key) dragRef.current = null; }}
                 style={{ left: d.left + (o?.dx ?? 0), top: d.top + (o?.dy ?? 0), color: d.color,
                          cursor: 'grab', touchAction: 'none', pointerEvents: 'auto', // .geom-label 의 pointer-events:none 오버라이드(드래그용)
                          transform: d.tx ? `translateX(${d.tx}%)` : undefined }}>
              <GeomLabel text={d.text} />
            </div>
          );
        })}
      </div>
    </div>
  );
}

// 라벨 폭 대략 추정(KaTeX 실측 전). LaTeX 명령을 렌더 글자수로 환산해야 정확:
// \cos·\sin·\log 등 함수명은 글자수만큼(cos=3), 그리스·기호(\theta·\pi)는 1글자.
// (이전엔 모든 \command 를 1글자로 봐서 "cos θ"·"sin θ" 박스가 너무 좁아 겹침 미검출.)
function estLabelWidth(text: string, fontPx: number): number {
  let t = String(text);
  t = t.replace(/\\(cos|sin|tan|sec|csc|cot|log|ln|lim|exp|max|min|sqrt|sup|inf|deg|arg|det|dim|gcd|lcm)\b/g,
                (_, w: string) => 'x'.repeat(w.length));   // 함수명 → 글자수
  t = t.replace(/\\[a-zA-Z]+/g, 'x');                       // 그리스·기타 명령 → 1글자
  t = t.replace(/[{}$^_\\\s]/g, '');                        // 구조문자 제거
  const n = Math.max(1, t.length);
  return Math.max(fontPx, n * fontPx * 0.6) + 8;
}

// 라벨 겹침 해소(de-overlap): 추정 박스가 겹치면 최소이동축으로 서로 밀어낸다(반복).
// 앵커에서 과도 이탈은 클램프(라벨이 가리키는 도형과 분리되지 않게). 캔버스 경계 내 유지.
// 노드 도식·LLM 채팅 공통(같은 Geometry 컴포넌트)이라 양쪽에 동시 적용된다.
type _LD = { key: string; text: string; left: number; top: number; tx: number; color?: string; fixed?: boolean };
type _Seg = [number, number, number, number];
// 선분 위에서 점(px,py)에 가장 가까운 점.
function _closestOnSeg(px: number, py: number, s: _Seg): [number, number] {
  const dx = s[2] - s[0], dy = s[3] - s[1];
  const len2 = dx * dx + dy * dy || 1;
  let t = ((px - s[0]) * dx + (py - s[1]) * dy) / len2;
  t = Math.max(0, Math.min(1, t));
  return [s[0] + t * dx, s[1] + t * dy];
}
function deOverlapLabels(descs: _LD[], fontPx: number, W: number, H: number, obstacles: _Seg[] = []): _LD[] {
  const h = fontPx * 1.5;
  // 앵커(좌표점)에서 라벨이 떠내려가는 최대 거리. 너무 크면 라벨이 좌표에서 멀어져
  // 무엇을 가리키는지 안 보인다. 겹침·장애물 회피에 필요한 최소(=박스 높이 ~2배)만 허용.
  const MAXSHIFT = fontPx * 2;
  const PAD = 2; // 라벨과 도형 사이 최소 여백
  const boxes = descs.map((d) => {
    const w = estLabelWidth(d.text, fontPx);
    const x0 = d.left + (d.tx / 100) * w;   // transform 반영한 시각 좌상단
    return { d, w, h, x: x0, y: d.top, ox: x0, oy: d.top, fixed: !!d.fixed };
  });
  for (let iter = 0; iter < 90; iter++) {
    let moved = false;
    // 1) 라벨끼리 겹침 — 최소이동축으로 분리. fixed 라벨(각 θ 등)은 안 움직이고 상대만 밀린다.
    for (let a = 0; a < boxes.length; a++) {
      for (let b = a + 1; b < boxes.length; b++) {
        const A = boxes[a], B = boxes[b];
        if (A.fixed && B.fixed) continue;
        const ox = Math.min(A.x + A.w, B.x + B.w) - Math.max(A.x, B.x);
        const oy = Math.min(A.y + A.h, B.y + B.h) - Math.max(A.y, B.y);
        if (ox > 0 && oy > 0) {
          moved = true;
          // fixed 쪽은 0, 자유 쪽이 전부 이동. 둘 다 자유면 반반.
          const wa = A.fixed ? 0 : (B.fixed ? 1 : 0.5), wb = B.fixed ? 0 : (A.fixed ? 1 : 0.5);
          if (ox <= oy) { const p = ox + 0.5, dir = A.x <= B.x ? -1 : 1; A.x += dir * p * wa; B.x -= dir * p * wb; }
          else { const p = oy + 0.5, dir = A.y <= B.y ? -1 : 1; A.y += dir * p * wa; B.y -= dir * p * wb; }
        }
      }
    }
    // 2) 라벨이 도형 외곽선(장애물)을 가리면 — 박스 밖으로 최소이동(MTV). fixed 는 면제.
    for (const box of boxes) {
      if (box.fixed) continue;
      const cx = box.x + box.w / 2, cy = box.y + box.h / 2;
      for (const seg of obstacles) {
        const [qx, qy] = _closestOnSeg(cx, cy, seg);
        const inX = qx > box.x - PAD && qx < box.x + box.w + PAD;
        const inY = qy > box.y - PAD && qy < box.y + box.h + PAD;
        if (inX && inY) {
          moved = true;
          const dl = qx - (box.x - PAD), dr = (box.x + box.w + PAD) - qx;
          const dt = qy - (box.y - PAD), db = (box.y + box.h + PAD) - qy;
          const m = Math.min(dl, dr, dt, db);
          if (m === dl) box.x += dl + 1; else if (m === dr) box.x -= dr + 1;
          else if (m === dt) box.y += dt + 1; else box.y -= db + 1;
        }
      }
    }
    if (!moved) break;
  }
  return boxes.map(({ d, w, h: bh, x, y, ox, oy }) => {
    let nx = Math.max(ox - MAXSHIFT, Math.min(ox + MAXSHIFT, x));
    let ny = Math.max(oy - MAXSHIFT, Math.min(oy + MAXSHIFT, y));
    nx = Math.max(0, Math.min(W - w, nx));
    ny = Math.max(0, Math.min(H - bh, ny));
    return { ...d, left: d.left + (nx - ox), top: d.top + (ny - oy) };
  });
}

// Public component used by ChatPanel; mirrors the Graph contract.
type Props = {
  spec: GeomSpec;
  width?: number;
  height?: number;
  onOpen?: () => void;
  interactive?: boolean;
  hideCaption?: boolean;
  noBroadcast?: boolean;   // sticky panel sets this to avoid bouncing back to latest on nav
  fixedWidth?: number;     // ResizeObserver 우회·고정폭 렌더(QA 시각 검수 하네스용)
};

export default function Geometry({ spec, width = DEFAULT_WIDTH, height = DEFAULT_HEIGHT, onOpen, interactive, hideCaption, noBroadcast, fixedWidth }: Props) {
  const clickable = !interactive && onOpen;
  // Mirror to the sticky side panel — same contract as PlotGraph/SvgGraph.
  // Skip when interactive (modal) OR when explicitly muted (sticky panel
  // re-rendering history: without the guard, prev/next would re-broadcast
  // the displayed entry and snap idx back to latest).
  useEffect(() => {
    if (interactive || noBroadcast) return;
    // Lazy import to keep the circular link (Graph imports Geometry) one-way
    // at module-init time.
    import('./Graph').then((m) => m.broadcastLatestGraph({ kind: 'geom', geomSpec: spec }));
  }, [spec, interactive, noBroadcast]);
  const node = <GeometryCanvas spec={spec} width={width} height={height} hideCaption={hideCaption} fixedWidth={fixedWidth} />;
  if (clickable) {
    return (
      <button type="button" onClick={onOpen} title="클릭하면 크게 봐요"
              className="block hover:ring-2 hover:ring-indigo-400/60 rounded-lg transition">
        {node}
      </button>
    );
  }
  return node;
}
