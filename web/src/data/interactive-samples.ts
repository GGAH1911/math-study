// Seed interactive specs — used by the verification page (§8) and as
// reference material in the LLM system prompt so the model learns the
// fence format from concrete, pedagogically meaningful examples.
//
// Spec convention: `"=expr"` anywhere a number or array is expected gets
// evaluated through mathjs against the live `scope`. The scope is computed
// from slider/param values and the optional `spec.scope` preamble.

import type { GeomSpec } from '../components/Geometry';
import type { Geom3DSpec } from '../components/Geometry3D';
import type { PlotSpec } from '../components/Graph';

export type InteractiveParam =
  | { name: string; label?: string; type: 'slider'; min: number; max: number; init: number; step?: number; unit?: string };

export type InteractiveReadout = {
  label: string;
  /** mathjs expression evaluated against the live scope. */
  expr: string;
  /** Decimal digits for the displayed number. Default 3. */
  digits?: number;
  unit?: string;
};

export type InteractiveSpec = {
  title?: string;
  params: InteractiveParam[];
  /** Optional mathjs preamble — `;`-separated assignments executed once
   *  per render. Defines auxiliary scope variables consumed by shapes. */
  scope?: string;
  /** Geometry block — shapes can use `"=expr"` for coords. */
  geometry?: GeomSpec;
  /** 3D geometry block — same `"=expr"` evaluation. Mutually exclusive with `geometry`. */
  geometry3d?: Geom3DSpec;
  /** Plot block — function strings stay as-is, slider values injected
   *  into each `fns[].scope` so function-plot evaluates with live params. */
  plot?: PlotSpec;
  /** Live readouts shown alongside the controls. */
  readout?: InteractiveReadout[];
};

// 1) 단위원과 삼각비 — θ를 0~360°로 돌리면서 cos/sin/tan 실시간 관찰
export const UNIT_CIRCLE: InteractiveSpec = {
  title: '단위원과 삼각비',
  params: [
    { name: 'theta', label: 'θ', type: 'slider', min: 0, max: 360, init: 30, step: 1, unit: '°' },
  ],
  scope: 'rad = theta * pi / 180; cx = cos(rad); sy = sin(rad)',
  geometry: {
    range: [-1.4, 1.4],
    yRange: [-1.4, 1.4],
    showAxes: true,
    showGrid: true,
    shapes: [
      { type: 'circle', center: [0, 0], radius: 1 },
      // sin (수직 보조선) — 점 P에서 x축으로 내린 수선
      { type: 'segment', from: ['=cx', 0] as unknown as [number, number],
        to: ['=cx', '=sy'] as unknown as [number, number], dashed: true, color: '#34d399' },
      // cos (수평 보조선) — 원점에서 x축 따라
      { type: 'segment', from: [0, 0], to: ['=cx', 0] as unknown as [number, number],
        color: '#fb7185' },
      // 반지름 OP
      { type: 'segment', from: [0, 0],
        to: ['=cx', '=sy'] as unknown as [number, number], color: '#a5b4fc' },
      // 점 P
      { type: 'point', at: ['=cx', '=sy'] as unknown as [number, number], label: 'P' },
    ],
  },
  readout: [
    { label: 'cos θ', expr: 'cx', digits: 3 },
    { label: 'sin θ', expr: 'sy', digits: 3 },
    { label: 'tan θ', expr: 'sy / cx', digits: 3 },
  ],
};

// 2) 함수 변환 — y = a · f(b(x - c)) + d. base f(x) = x²
// a/b/c/d 슬라이더로 신축·평행이동 효과 직접 체험.
export const FUNCTION_TRANSFORM: InteractiveSpec = {
  title: '함수 변환 $y = a \\cdot f(b(x - c)) + d$, $f(x) = x^2$',
  params: [
    { name: 'a', label: 'a', type: 'slider', min: -3, max: 3, init: 1, step: 0.1 },
    { name: 'b', label: 'b', type: 'slider', min: -3, max: 3, init: 1, step: 0.1 },
    { name: 'c', label: 'c', type: 'slider', min: -3, max: 3, init: 0, step: 0.1 },
    { name: 'd', label: 'd', type: 'slider', min: -3, max: 3, init: 0, step: 0.1 },
  ],
  plot: {
    range: [-5, 5],
    yRange: [-5, 8],
    fns: [
      { fn: 'x^2', label: '$f(x) = x^2$', color: '#71717a' },
      { fn: 'a * (b * (x - c))^2 + d', label: '$a f(b(x-c)) + d$' },
    ],
  },
  readout: [
    { label: '꼭짓점 x', expr: 'c', digits: 2 },
    { label: '꼭짓점 y', expr: 'd', digits: 2 },
    { label: '개구 방향', expr: 'sign(a)' },
  ],
};

// 3) 미분계수와 접선 — 점 a 를 슬라이더로 이동, 접선 기울기 = f'(a)
// f(x) = x³ - 3x. f'(x) = 3x² - 3.
export const DERIVATIVE_TANGENT: InteractiveSpec = {
  title: '$f(x) = x^3 - 3x$의 점 $a$에서의 접선',
  params: [
    { name: 'a', label: 'a', type: 'slider', min: -2.5, max: 2.5, init: 1, step: 0.05 },
  ],
  scope: "fa = a^3 - 3*a; dfa = 3*a^2 - 3",
  plot: {
    range: [-3, 3],
    yRange: [-5, 5],
    fns: [
      { fn: 'x^3 - 3*x', label: '$f(x)$' },
      // 접선: y = f'(a)(x - a) + f(a) = (3a² - 3)x - 2a³
      { fn: '(3*a^2 - 3)*(x - a) + a^3 - 3*a', label: '점 $a$의 접선' },
    ],
    points: [['=a', '=fa']] as unknown as Array<[number, number]>,
    pointsLabel: '$(a, f(a))$',
  },
  readout: [
    { label: 'f(a)', expr: 'fa', digits: 3 },
    { label: "f'(a) (기울기)", expr: 'dfa', digits: 3 },
    { label: '접선 절편', expr: 'fa - dfa * a', digits: 3 },
  ],
};

// 4) 정적분 면적 — f(x) = x² - 2x + 2 (항상 양수), 구간 [a, b]
// closed: true + range로 음영 표시.
export const INTEGRAL_AREA: InteractiveSpec = {
  title: '정적분 $\\int_a^b (x^2 - 2x + 2) \\, dx$',
  params: [
    { name: 'a', label: 'a', type: 'slider', min: -2, max: 4, init: 0, step: 0.1 },
    { name: 'b', label: 'b', type: 'slider', min: -2, max: 4, init: 3, step: 0.1 },
  ],
  // 정확한 부정적분: F(x) = x³/3 - x² + 2x → ∫ₐᵇ = F(b) - F(a)
  scope: "Fa = a^3/3 - a^2 + 2*a; Fb = b^3/3 - b^2 + 2*b; area = Fb - Fa",
  plot: {
    range: [-2, 4],
    yRange: [0, 10],
    fns: [
      { fn: 'x^2 - 2*x + 2', label: '$f(x)$', color: '#71717a' },
      // closed + range: [a, b] → [a, b] 구간만 음영. `=expr`을 range에 넣어
      // Interactive가 슬라이더로 resolve.
      { fn: 'x^2 - 2*x + 2', label: '음영', color: '#a5b4fc', closed: true,
        range: ['=a', '=b'] as unknown as [number, number] },
    ],
  },
  readout: [
    { label: '면적 ∫', expr: 'area', digits: 3 },
    { label: 'f(a)', expr: 'a^2 - 2*a + 2', digits: 2 },
    { label: 'f(b)', expr: 'b^2 - 2*b + 2', digits: 2 },
  ],
};

// 5) 벡터 합성 — 두 벡터의 끝점을 슬라이더로 조정, u + v 합 벡터 + 크기/각도
export const VECTOR_SUM: InteractiveSpec = {
  title: '벡터 합 $\\vec{u} + \\vec{v}$',
  params: [
    { name: 'ux', label: 'uₓ', type: 'slider', min: -3, max: 3, init: 2, step: 0.1 },
    { name: 'uy', label: 'uᵧ', type: 'slider', min: -3, max: 3, init: 1, step: 0.1 },
    { name: 'vx', label: 'vₓ', type: 'slider', min: -3, max: 3, init: -1, step: 0.1 },
    { name: 'vy', label: 'vᵧ', type: 'slider', min: -3, max: 3, init: 2, step: 0.1 },
  ],
  scope: "sx = ux + vx; sy = uy + vy; mag = sqrt(sx^2 + sy^2); ang = atan2(sy, sx) * 180 / pi",
  geometry: {
    range: [-4, 4],
    yRange: [-3, 4],
    showAxes: true,
    showGrid: true,
    shapes: [
      { type: 'vector', from: [0, 0],
        to: ['=ux', '=uy'] as unknown as [number, number],
        label: '$\\vec{u}$', color: '#34d399' },
      { type: 'vector', from: [0, 0],
        to: ['=vx', '=vy'] as unknown as [number, number],
        label: '$\\vec{v}$', color: '#fb7185' },
      // 합 벡터 — 원점에서 (ux+vx, uy+vy)
      { type: 'vector', from: [0, 0],
        to: ['=sx', '=sy'] as unknown as [number, number],
        label: '$\\vec{u}+\\vec{v}$', color: '#a5b4fc' },
      // 평행사변형 점선: u 끝에서 v 만큼, v 끝에서 u 만큼 이동
      { type: 'segment',
        from: ['=ux', '=uy'] as unknown as [number, number],
        to: ['=sx', '=sy'] as unknown as [number, number],
        dashed: true, color: '#52525b' },
      { type: 'segment',
        from: ['=vx', '=vy'] as unknown as [number, number],
        to: ['=sx', '=sy'] as unknown as [number, number],
        dashed: true, color: '#52525b' },
    ],
  },
  readout: [
    { label: '$|\\vec{u}+\\vec{v}|$', expr: 'mag', digits: 3 },
    { label: '방향 (°)', expr: 'ang', digits: 1 },
    { label: '$\\vec{u}\\cdot\\vec{v}$ (내적)', expr: 'ux*vx + uy*vy', digits: 2 },
  ],
};

// 6) 정규분포 — μ, σ 슬라이더 → 곡선 변형 + 약 68/95 영역 시각화
export const NORMAL_DIST: InteractiveSpec = {
  title: '정규분포 $N(\\mu, \\sigma^2)$',
  params: [
    { name: 'mu',    label: 'μ', type: 'slider', min: -3, max: 3, init: 0, step: 0.1 },
    { name: 'sigma', label: 'σ', type: 'slider', min: 0.3, max: 3, init: 1, step: 0.1 },
  ],
  scope: "peak = 1 / (sigma * sqrt(2*pi))",
  plot: {
    range: [-6, 6],
    yRange: [0, 1.4],
    fns: [
      // PDF
      { fn: '(1 / (sigma * sqrt(2*pi))) * exp(-((x - mu)^2) / (2 * sigma^2))',
        label: '$\\varphi(x)$' },
      // μ ± σ 음영
      { fn: '(1 / (sigma * sqrt(2*pi))) * exp(-((x - mu)^2) / (2 * sigma^2))',
        closed: true, color: '#a5b4fc', label: '음영 (μ−σ ~ μ+σ)',
        range: ['=mu - sigma', '=mu + sigma'] as unknown as [number, number] },
    ],
  },
  readout: [
    { label: '평균 μ', expr: 'mu', digits: 2 },
    { label: '표준편차 σ', expr: 'sigma', digits: 2 },
    { label: '최대값 φ(μ)', expr: 'peak', digits: 3 },
  ],
};

export const INTERACTIVE_SAMPLES: ReadonlyArray<{ key: string; spec: InteractiveSpec }> = [
  { key: 'unit_circle',         spec: UNIT_CIRCLE },
  { key: 'function_transform',  spec: FUNCTION_TRANSFORM },
  { key: 'derivative_tangent',  spec: DERIVATIVE_TANGENT },
  { key: 'integral_area',       spec: INTEGRAL_AREA },
  { key: 'vector_sum',          spec: VECTOR_SUM },
  { key: 'normal_dist',         spec: NORMAL_DIST },
];
