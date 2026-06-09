// Graph renderer for chat messages.
//
// LLM emits one of two fenced code blocks inside its responses:
//
//   ```plot
//   {"fn": "x^2 - 3x + 2", "range": [-1, 4], "yRange": [-2, 6]}
//   ```
//
//   ```svg
//   <svg viewBox="0 0 200 200">...</svg>
//   ```
//
// ChatPanel detects these and renders <Graph kind="plot" | "svg" .../> inline.
// Clicking the inline rendering opens a modal with the full-size version,
// and the most-recent graph is mirrored into a sticky side panel on desktop.

import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import Geometry, { type GeomSpec } from './Geometry';
import Geometry3D, { type Geom3DSpec } from './Geometry3D';
import Numberline, { type NumberlineSpec } from './Numberline';
import StatsChart, { type ChartSpec } from './StatsChart';
import Interactive from './Interactive';
import type { InteractiveSpec } from '../data/interactive-samples';
import { MathishText, ensureKatex } from '../lib/mathish';
import { PLOT_COLORS } from '../lib/palette';

// -------------------------------------------------------------- types

export type PlotSpec = {
  fn?: string;
  fns?: Array<{
    fn: string;
    color?: string;
    closed?: boolean;            // fill the area between fn and x-axis
    label?: string;
    range?: [number, number];    // restrict the fn to this x-interval
                                  // (useful for shading ∫ from a to b)
    nSamples?: number;
    scope?: Record<string, number>;  // mathjs scope (parameters)
  }>;
  range?: [number, number];      // x-axis
  yRange?: [number, number];     // y-axis (auto if omitted)
  points?: Array<[number, number]>;
  pointsLabel?: string;
  // 교점·근 자동 계산 — LLM 이 좌표를 손계산하면 거의 틀리므로(교점은 특히),
  // 두 함수(또는 한 함수)와 대략적 bracket 구간만 받아 렌더러가 이분법으로 정확히 푼다.
  // 결과 좌표는 points 와 합쳐져 같은 빨간 점으로 찍힌다.
  intersections?: Array<{ f: string; g: string; in: [number, number]; label?: string }>;
  roots?: Array<{ fn: string; in: [number, number]; label?: string }>;
  title?: string;
  grid?: boolean;
  // Optional sliders shown in the modal — each binds a name in fn scope.
  sliders?: Array<{ name: string; min: number; max: number; step?: number; init?: number }>;
};

// Persist + broadcast a small rolling history of recent graphs so the
// floating sticky panel can show prev/next navigation and survives page
// transitions.
const HISTORY_KEY = 'math-study:graph-history';
const HISTORY_MAX = 12;

export type GraphHistoryEntry = {
  kind: 'plot' | 'svg' | 'geom' | 'geom3d' | 'numberline' | 'chart' | 'interactive';
  spec?: PlotSpec;
  svg?: string;
  geomSpec?: GeomSpec;
  geom3dSpec?: Geom3DSpec;
  numberlineSpec?: NumberlineSpec;
  chartSpec?: ChartSpec;
  interactiveSpec?: InteractiveSpec;
  ts: number;             // when it was added (epoch ms)
  source?: string;        // optional context (e.g. concept slug)
};

declare global {
  interface WindowEventMap {
    'math-study:graph': CustomEvent<GraphHistoryEntry>;
  }
}

// Validate an entry has enough data to actually render. Drops orphan/empty
// entries left over from earlier code paths (e.g. a plot broadcast that had
// no fn/fns, now correctly rejected at render time but still in localStorage).
function isValidEntry(e: GraphHistoryEntry | null | undefined): boolean {
  if (!e || typeof e !== 'object') return false;
  if (e.kind === 'plot') {
    const s = e.spec;
    if (!s) return false;
    const hasFn = !!s.fn || (Array.isArray(s.fns) && s.fns.length > 0);
    const hasPts = Array.isArray(s.points) && s.points.length > 0;
    return hasFn || hasPts;
  }
  if (e.kind === 'svg') return typeof e.svg === 'string' && e.svg.trim().length > 0;
  if (e.kind === 'geom') return !!e.geomSpec && Array.isArray(e.geomSpec.shapes) && e.geomSpec.shapes.length > 0;
  if (e.kind === 'geom3d') return !!e.geom3dSpec && Array.isArray(e.geom3dSpec.shapes) && e.geom3dSpec.shapes.length > 0;
  if (e.kind === 'numberline') {
    const s = e.numberlineSpec;
    if (!s || !Array.isArray(s.range) || s.range.length !== 2) return false;
    const m = Array.isArray(s.marks) ? s.marks.length : 0;
    const iv = Array.isArray(s.intervals) ? s.intervals.length : 0;
    return m + iv > 0;
  }
  if (e.kind === 'chart') return !!e.chartSpec && typeof e.chartSpec.kind === 'string';
  if (e.kind === 'interactive') {
    const s = e.interactiveSpec;
    if (!s || !Array.isArray(s.params)) return false;
    // 하나라도 render target 있으면 통과 (geometry / geometry3d / plot).
    const hasGeom2d = !!s.geometry && Array.isArray(s.geometry.shapes);
    const hasGeom3d = !!s.geometry3d && Array.isArray(s.geometry3d.shapes);
    const hasPlot = !!s.plot;
    return hasGeom2d || hasGeom3d || hasPlot;
  }
  return false;
}

// JSON serde sentinels for ±Infinity (which JSON.stringify turns into `null`
// — that silently flipped Numberline interval direction in the sticky panel).
const INF_SENTINEL = '__INF__';
const NEG_INF_SENTINEL = '__NEG_INF__';
function infReplacer(_key: string, value: unknown) {
  if (value === Infinity) return INF_SENTINEL;
  if (value === -Infinity) return NEG_INF_SENTINEL;
  return value;
}
function infReviver(_key: string, value: unknown) {
  if (value === INF_SENTINEL) return Infinity;
  if (value === NEG_INF_SENTINEL) return -Infinity;
  return value;
}

function loadHistory(): GraphHistoryEntry[] {
  try {
    const raw = window.localStorage.getItem(HISTORY_KEY);
    if (!raw) return [];
    const arr = JSON.parse(raw, infReviver) as GraphHistoryEntry[];
    if (!Array.isArray(arr)) return [];
    // Filter out malformed entries from older sessions; persist the cleanup
    // so subsequent loads don't re-skip them.
    const valid = arr.filter(isValidEntry).slice(-HISTORY_MAX);
    if (valid.length !== arr.length) {
      try { window.localStorage.setItem(HISTORY_KEY, JSON.stringify(valid, infReplacer)); } catch { /* quota */ }
    }
    return valid;
  } catch { return []; }
}
function saveHistory(h: GraphHistoryEntry[]) {
  try { window.localStorage.setItem(HISTORY_KEY, JSON.stringify(h.slice(-HISTORY_MAX), infReplacer)); }
  catch { /* quota */ }
}

export function broadcastLatestGraph(g: {
  kind: 'plot' | 'svg' | 'geom' | 'geom3d' | 'numberline' | 'chart' | 'interactive';
  spec?: PlotSpec; svg?: string;
  geomSpec?: GeomSpec; geom3dSpec?: Geom3DSpec;
  numberlineSpec?: NumberlineSpec; chartSpec?: ChartSpec;
  interactiveSpec?: InteractiveSpec;
}) {
  const entry: GraphHistoryEntry = { ...g, ts: Date.now() };
  // Don't pollute history with entries the panel can't render.
  if (!isValidEntry(entry)) return;
  const hist = loadHistory();
  // De-dup: if the most-recent entry is structurally identical, skip.
  const last = hist[hist.length - 1];
  const same = last && last.kind === entry.kind &&
    JSON.stringify(last.spec ?? null) === JSON.stringify(entry.spec ?? null) &&
    JSON.stringify(last.geomSpec ?? null) === JSON.stringify(entry.geomSpec ?? null) &&
    JSON.stringify(last.geom3dSpec ?? null) === JSON.stringify(entry.geom3dSpec ?? null) &&
    JSON.stringify(last.numberlineSpec ?? null) === JSON.stringify(entry.numberlineSpec ?? null) &&
    JSON.stringify(last.chartSpec ?? null) === JSON.stringify(entry.chartSpec ?? null) &&
    JSON.stringify(last.interactiveSpec ?? null) === JSON.stringify(entry.interactiveSpec ?? null) &&
    (last.svg ?? '') === (entry.svg ?? '');
  if (!same) {
    hist.push(entry);
    saveHistory(hist);
  }
  window.dispatchEvent(new CustomEvent('math-study:graph', { detail: entry }));
}

// -------------------------------------------------------------- function-plot helper

let FN_PLOT_LOADER: Promise<typeof import('function-plot').default> | null = null;
function loadFunctionPlot() {
  if (!FN_PLOT_LOADER) {
    FN_PLOT_LOADER = import('function-plot').then((m) => m.default ?? (m as unknown as typeof import('function-plot').default));
  }
  return FN_PLOT_LOADER;
}

// Lazy mathjs evaluator (function-plot bundles it but doesn't expose).
type MathEvalFn = (expr: string, scope: object) => number;
let MATH_EVAL: MathEvalFn | null = null;
let MATH_LOADER: Promise<MathEvalFn | null> | null = null;
function loadMathEval() {
  if (!MATH_LOADER) {
    MATH_LOADER = import('mathjs')
      .then((mod) => {
        const fn = (mod as unknown as { evaluate: (e: string, s: object) => number }).evaluate;
        MATH_EVAL = fn;
        return fn;
      })
      .catch(() => null);
  }
  return MATH_LOADER;
}

// 솔버 입력 정규화 — LLM 이 박는 유니코드 수학기호 → mathjs ASCII.
function normExpr(s: string): string {
  return s.replace(/√/g, 'sqrt').replace(/π/g, 'pi')
    .replace(/×/g, '*').replace(/÷/g, '/').replace(/−/g, '-').replace(/[⋅·]/g, '*');
}

// 이분법 근 찾기 — bracket [a0,b0] 에서 expr(x)=0 의 근. 양 끝 부호가 안 갈리면
// 256분할 스캔으로 부호 바뀌는 sub-bracket 을 먼저 찾고 이분한다. 미분 불필요(견고).
// LLM 의 손계산 교점 좌표를 결정적 계산으로 대체하기 위한 핵심 루틴.
function bisectRoot(expr: string, a0: number, b0: number,
                    evalFn: (e: string, s: object) => number): number | null {
  const f = (x: number): number => {
    try { const v = evalFn(expr, { x }); return typeof v === 'number' ? v : NaN; }
    catch { return NaN; }
  };
  let a = a0, b = b0, fa = f(a), fb = f(b);
  if (!(Number.isFinite(fa) && Number.isFinite(fb) && fa * fb <= 0)) {
    const N = 256; let pa = a0, pf = f(a0), ok = false;
    for (let i = 1; i <= N; i++) {
      const x = a0 + ((b0 - a0) * i) / N, fx = f(x);
      if (Number.isFinite(pf) && Number.isFinite(fx) && pf * fx <= 0) {
        a = pa; b = x; fa = pf; fb = fx; ok = true; break;
      }
      pa = x; pf = fx;
    }
    if (!ok) return null;
  }
  for (let i = 0; i < 100; i++) {
    const m = (a + b) / 2, fm = f(m);
    if (!Number.isFinite(fm)) return null;
    if (Math.abs(fm) < 1e-12 || b - a < 1e-12) return m;
    if (fa * fm <= 0) { b = m; fb = fm; } else { a = m; fa = fm; }
  }
  return (a + b) / 2;
}

// intersections/roots 스펙 → 실제 점 좌표. 점근선을 가로지른 가짜 근(|f-g| 큰 곳)은
// 검증(eval 후 실제로 0 / f≈g 인지)으로 버린다 → tan 같은 주기함수도 안전.
function solvePlotPoints(spec: PlotSpec,
                         evalFn: ((e: string, s: object) => number) | null): Array<[number, number]> {
  if (!evalFn) return [];
  const out: Array<[number, number]> = [];
  for (const it of spec.intersections ?? []) {
    const f = normExpr(it.f), g = normExpr(it.g);
    const x = bisectRoot(`(${f})-(${g})`, it.in[0], it.in[1], evalFn);
    if (x == null) continue;
    let fy = NaN, gy = NaN;
    try { const a = evalFn(f, { x }); if (typeof a === 'number') fy = a; } catch { /* */ }
    try { const b = evalFn(g, { x }); if (typeof b === 'number') gy = b; } catch { /* */ }
    if (Number.isFinite(x) && Number.isFinite(fy) && Number.isFinite(gy)
        && Math.abs(fy - gy) < 1e-3 * (1 + Math.abs(fy))) out.push([x, fy]);
  }
  for (const it of spec.roots ?? []) {
    const fn = normExpr(it.fn);
    const x = bisectRoot(fn, it.in[0], it.in[1], evalFn);
    if (x == null) continue;
    let y = NaN;
    try { const v = evalFn(fn, { x }); if (typeof v === 'number') y = v; } catch { /* */ }
    if (Number.isFinite(x) && Number.isFinite(y) && Math.abs(y) < 1e-3) out.push([x, 0]);
  }
  return out;
}

// -------------------------------------------------------------- SVG sanitizer

let DOMPURIFY_LOADER: Promise<typeof import('dompurify').default> | null = null;
function loadDOMPurify() {
  if (!DOMPURIFY_LOADER) {
    DOMPURIFY_LOADER = import('dompurify').then((m) => m.default ?? (m as unknown as typeof import('dompurify').default));
  }
  return DOMPURIFY_LOADER;
}

function sanitizeSvg(raw: string, purifier: typeof import('dompurify').default | null): string {
  if (!purifier) return ''; // refuse if loader failed
  return purifier.sanitize(raw, {
    USE_PROFILES: { svg: true, svgFilters: true },
    FORBID_TAGS: ['script', 'foreignObject'],
    FORBID_ATTR: ['onload', 'onclick', 'onerror'],
  }) as unknown as string;
}

// Ensure the root <svg> has width/height attributes — without them an SVG
// with only viewBox renders at the browser default (300×150) inside an
// inline-block, or collapses to 0 in some layout contexts. We honor existing
// width/height if present and otherwise inject the requested container size
// while preserving the viewBox aspect via `preserveAspectRatio`.
function ensureSvgDimensions(html: string, width: number, height: number): string {
  if (!html) return html;
  const match = html.match(/<svg\b([^>]*)>/i);
  if (!match) return html;
  const attrs = match[1];
  const hasWidth = /\swidth\s*=/.test(attrs);
  const hasHeight = /\sheight\s*=/.test(attrs);
  if (hasWidth && hasHeight) return html;
  const inject: string[] = [];
  if (!hasWidth) inject.push(`width="${width}"`);
  if (!hasHeight) inject.push(`height="${height}"`);
  inject.push('style="max-width:100%;height:auto"');
  return html.replace(/<svg\b([^>]*)>/i, `<svg$1 ${inject.join(' ')}>`);
}

// -------------------------------------------------------------- Graph component

type GraphProps = {
  kind: 'plot' | 'svg';
  spec?: PlotSpec;
  svg?: string;
  width?: number;
  height?: number;
  onOpen?: () => void;
  interactive?: boolean;   // when in modal, allow zoom/pan via function-plot
  hideCaption?: boolean;
  noBroadcast?: boolean;   // suppress sticky-panel mirroring (used by the
                            // sticky panel itself when re-rendering history,
                            // so navigation doesn't re-broadcast and jump
                            // the index back to latest)
};

function Caption({ text, large = false }: { text?: string; large?: boolean }) {
  if (!text) return null;
  return (
    <div className={`break-keep px-1 ${large ? 'text-sm text-zinc-100 mb-2 font-semibold' : 'text-[11px] text-zinc-300 mb-1'}`}>
      <MathishText text={text} />
    </div>
  );
}

function PlotGraph({ spec, width = 360, height = 220, interactive = false, hideCaption = false }: { spec: PlotSpec; width?: number; height?: number; interactive?: boolean; hideCaption?: boolean }) {
  const ref = useRef<HTMLDivElement | null>(null);
  const wrapRef = useRef<HTMLDivElement | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [effWidth, setEffWidth] = useState<number>(width);

  // Slider values keyed by name; only meaningful in interactive (modal) mode.
  const [sliderValues, setSliderValues] = useState<Record<string, number>>(() => {
    const init: Record<string, number> = {};
    for (const s of spec.sliders ?? []) init[s.name] = s.init ?? (s.min + s.max) / 2;
    return init;
  });

  // Responsive — clamp to parent's actual width so the SVG never overflows
  // the message bubble or sticky panel. Re-measure on resize.
  //
  // Hardened against ResizeObserver feedback loops: (1) round to an integer
  // and only setState on a ≥1px change, so subpixel oscillation can't keep
  // re-triggering the expensive function-plot rebuild (the render effect below
  // depends on effWidth); (2) rAF-throttle the RO callback so a burst of
  // notifications — e.g. while an image-heavy page churns layout — coalesces
  // into one measure and is deferred OUT of the RO delivery cycle. Without
  // this the RO→setState→rebuild→RO cycle pegs the main thread (hard freeze)
  // when the panel is open over a churning page like /problems.
  useEffect(() => {
    const el = wrapRef.current;
    if (!el) return;
    let raf = 0;
    const measure = () => {
      raf = 0;
      const pw = el.parentElement?.clientWidth ?? width;
      const target = Math.round(Math.min(width, Math.max(220, pw - 16)));
      setEffWidth((prev) => (Math.abs(prev - target) < 1 ? prev : target));
    };
    measure();
    const ro = new ResizeObserver(() => {
      if (!raf) raf = requestAnimationFrame(measure);
    });
    if (el.parentElement) ro.observe(el.parentElement);
    return () => { if (raf) cancelAnimationFrame(raf); ro.disconnect(); };
  }, [width]);

  // Resolve fn list + assigned colors once so legend + chart stay in sync.
  const resolvedFns = useMemo(() => {
    const raw = spec.fns ?? (spec.fn ? [{ fn: spec.fn }] : []);
    return raw.map((f, i) => ({
      fn: f.fn,
      color: f.color ?? PLOT_COLORS[i % PLOT_COLORS.length],
      closed: f.closed,
      label: f.label ?? f.fn,
      range: f.range,
      nSamples: f.nSamples,
      scope: f.scope,
    }));
  }, [spec.fns, spec.fn]);

  // Surface bad spec immediately (no need to wait for function-plot lazy load
  // before showing the user that fn/fns is missing).
  if (resolvedFns.length === 0 && (spec.points?.length ?? 0) === 0) {
    return (
      <pre className="text-xs text-rose-300 bg-rose-500/10 border border-rose-500/30 p-2 rounded">
        plot spec needs `fn` or `fns`
      </pre>
    );
  }

  // Kick off mathjs load in parallel with function-plot
  useEffect(() => { loadMathEval(); }, []);

  useEffect(() => {
    let cancelled = false;
    setErr(null);
    Promise.all([loadFunctionPlot(), loadMathEval()]).then(([fp, evalFn]) => {
      if (cancelled || !ref.current) return;
      ref.current.innerHTML = '';
      try {
        if (resolvedFns.length === 0) {
          setErr('plot spec needs `fn` or `fns`');
          return;
        }
        // function-plot 의 기본 `interval` 샘플러(구간연산)는 `pow(interval,
        // interval)` 즉 **변수 지수** `(...)^x`·`a^x`·`x^x` 를 평가하지 못해
        // 선을 통째로 안 그린다(NaN 구간 반환). 그런데 hover 툴팁은 mathjs 로
        // 따로 재계산하므로 "선은 안 보이는데 hover 하면 값이 뜨는" 증상이 됨.
        // → 지수에 변수(letter)가 있으면 `polyline`(builtIn 선형 샘플러, 점마다
        //   실제 평가)로 전환. 상수 지수(`x^2`)는 asymptote 처리가 나은 interval 유지.
        const hasVarExponent = (s: string) => /(\^|\*\*)\s*\(?[^)\s,]*[a-zA-Z]/.test(s);
        const data = resolvedFns.map((f) => {
          const d: Record<string, unknown> = { fn: f.fn, color: f.color };
          if (f.closed) {
            d.closed = true;
            // Translucent fill when closed — derive from line color
            d.color = f.color;
          }
          if (hasVarExponent(f.fn)) {
            d.graphType = 'polyline';
            if (!f.nSamples) d.nSamples = 1000;
          }
          if (f.range) d.range = f.range;
          if (f.nSamples) d.nSamples = f.nSamples;
          if (f.scope) d.scope = { ...f.scope, ...sliderValues };
          else if (Object.keys(sliderValues).length) d.scope = sliderValues;
          return d;
        });
        // 교점·근은 렌더러가 결정적으로 계산(LLM 손계산 대체) → literal points 와 합침.
        const solvedPoints = solvePlotPoints(spec, evalFn);
        const allPoints = [...(spec.points ?? []), ...solvedPoints];
        const points = allPoints.length > 0
          ? [{ points: allPoints, fnType: 'points', graphType: 'scatter', color: '#f43f5e' }]
          : [];
        // Add invisible (visually merged with origin-axis line) function
        // entries for y=0 and x=0 so that function-plot's tip will snap
        // to those lines too. Without these, hovering over the axis lines
        // doesn't trigger any snap.
        // `?? [-5,5]` only catches null/undefined — an LLM-emitted `range: []`
        // or `range: [3]` is truthy and would slip through, producing a broken
        // (empty/single-element) d3 domain. Require exactly two finite numbers.
        const validRange = (r: unknown): r is [number, number] =>
          Array.isArray(r) && r.length === 2 && r.every((n) => typeof n === 'number' && Number.isFinite(n));
        const xRange: [number, number] = validRange(spec.range) ? spec.range : [-5, 5];
        const yRangeForAxes: [number, number] = validRange(spec.yRange) ? spec.yRange : [-10, 10];
        const axisData: Array<Record<string, unknown>> = [];
        if (yRangeForAxes[0] <= 0 && yRangeForAxes[1] >= 0) {
          axisData.push({ fn: '0', color: '#fafafa', skipTip: false });
        }
        if (xRange[0] <= 0 && xRange[1] >= 0) {
          // Vertical line x=0 via parametric — function-plot requires
          // graphType:'polyline' so it samples via the builtIn sampler
          // instead of the (incompatible) interval sampler.
          axisData.push({
            fnType: 'parametric',
            x: '0',
            y: 't',
            range: yRangeForAxes,
            color: '#fafafa',
            graphType: 'polyline',
          });
        }

        // "Nice" grid step from the visible x-range — picks one of
        // {1, 0.5, 0.25, 0.2, 0.1, 0.05, ...} so coordinates snap to a
        // human-readable position. ~25 steps across the visible range.
        const niceStep = (span: number): number => {
          const target = span / 25;
          const candidates = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05,
                              0.1, 0.2, 0.25, 0.5, 1, 2, 5, 10, 20, 50, 100];
          for (const c of candidates) if (c >= target) return c;
          return 100;
        };
        const xStep = niceStep(xRange[1] - xRange[0]);

        // Concatenated list — tip renderer receives the *index* into the
        // combined data array, so we keep the same ordering everywhere.
        const allData = [...data, ...axisData, ...(points as never[])];

        const fmt = (v: number) => {
          if (!Number.isFinite(v)) return '?';
          const s = Math.abs(v) >= 100 ? v.toFixed(0) : v.toFixed(2);
          return s.includes('.') ? s.replace(/\.?0+$/, '') : s;
        };

        const inst = fp({
          target: ref.current,
          width: effWidth,
          height,
          xAxis: { domain: xRange },
          yAxis: validRange(spec.yRange) ? { domain: spec.yRange } : undefined,
          grid: spec.grid !== false,
          // title rendered above by <Caption />
          disableZoom: !interactive,
          // Cursor crosshair + snap to closest function value. We round
          // x to the grid step, then *recompute* y by evaluating the
          // hovered function at that rounded x — gives mathematically
          // exact (1.5, 2.5) instead of sampler's (1.84, 0.51).
          tip: {
            xLine: true,
            yLine: true,
            renderer: (x: number, y: number, index: number) => {
              const item = allData[index] as { fn?: string; fnType?: string; scope?: Record<string, number> };
              let xr = Math.round(x / xStep) * xStep;
              let yr = y;
              if (item?.fnType === 'parametric') {
                // x=0 axis line
                xr = 0;
                yr = Math.round(y / xStep) * xStep;
              } else if (item?.fn && MATH_EVAL) {
                // Re-evaluate with the SAME scope (slider/param values) the
                // sampler used — otherwise `a*x` etc. resolves `a` to NaN.
                // mathjs returns a Complex object (not a number) outside the
                // real domain (e.g. sqrt/log of a negative); fall back to the
                // sampler's y in that case instead of showing "?".
                try {
                  const v = MATH_EVAL(item.fn, { x: xr, ...(item.scope ?? {}) });
                  yr = typeof v === 'number' && Number.isFinite(v) ? v : Math.round(y / xStep) * xStep;
                } catch { yr = Math.round(y / xStep) * xStep; }
              } else {
                yr = Math.round(y / xStep) * xStep;
              }
              return `(${fmt(xr)}, ${fmt(yr)})`;
            },
          },
          data: allData,
        });

        // Origin axes (y=0 and x=0) are now part of the function-plot data
        // above, so they get drawn automatically + participate in tip
        // snapping. No manual SVG append needed.
        // Post-style the SVG. function-plot writes inline `style` attrs in
        // some places (notably `.domain` for axes), so we go via .style.*
        // first, then fall back to setAttribute. This makes the axis lines
        // visibly stand out on the dark background.
        const svg = ref.current.querySelector('svg');
        if (svg) {
          const force = (els: NodeListOf<Element>, props: Record<string, string>) => {
            els.forEach((node) => {
              const el = node as SVGElement & { style: CSSStyleDeclaration };
              for (const [k, v] of Object.entries(props)) {
                try { el.style.setProperty(k, v, 'important'); } catch { /* noop */ }
                el.setAttribute(k, v);
              }
            });
          };
          // Outer axis line (the actual visible x= and y= rule)
          force(svg.querySelectorAll('.x.axis path.domain, .y.axis path.domain, .axis path.domain'),
                { stroke: '#fafafa', 'stroke-width': '1.6', fill: 'none' });
          // Tick stub lines on the axis
          force(svg.querySelectorAll('.x.axis g.tick line, .y.axis g.tick line'),
                { stroke: '#a1a1aa', 'stroke-width': '1' });
          // Tick value labels
          force(svg.querySelectorAll('.axis g.tick text, .axis text'),
                { fill: '#fafafa', 'font-size': '11', 'font-weight': '500' });
          // Background grid (paler so the data dominates)
          force(svg.querySelectorAll('.graph .grid line, g.grid line'),
                { stroke: '#3f3f46', 'stroke-width': '0.5' });
          // Function curves a bit thicker
          force(svg.querySelectorAll('.graph .line path, path.line, g.graph path'),
                { 'stroke-width': '2.25' });
          // Scatter points (e.g. roots of f) — function-plot defaults are
          // tiny dots that nearly disappear at small sizes. Force them to
          // a clearly visible radius + outline. fill explicit so contrast
          // doesn't depend on function-plot's internal defaults.
          force(svg.querySelectorAll('g.graph circle, .graph circle'),
                { r: '5', fill: '#f43f5e', stroke: '#fafafa', 'stroke-width': '1.5' });
          // Crosshair lines on hover (from `tip.xLine`/`yLine`)
          force(svg.querySelectorAll('.tip-x-line, .tip-y-line, .tip line'),
                { stroke: '#a5b4fc', 'stroke-width': '1', 'stroke-dasharray': '4 3' });
        }
      } catch (e) {
        setErr((e as Error).message ?? 'plot failed');
      }
    }).catch((e) => {
      if (!cancelled) setErr(String(e));
    });
    return () => { cancelled = true; };
  }, [resolvedFns, spec.points, spec.intersections, spec.roots, spec.range, spec.yRange, spec.grid, effWidth, height, interactive, sliderValues]);

  if (err) {
    return <pre className="text-xs text-rose-300 bg-rose-500/10 border border-rose-500/30 p-2 rounded">{err}</pre>;
  }
  return (
    <div
      ref={wrapRef}
      className="graph-host bg-zinc-950 border border-zinc-700/80 rounded-lg shadow-inner max-w-full"
      style={{ padding: '10px 12px' }}
    >
      {!hideCaption && <Caption text={spec.title} />}
      <div ref={ref} className="graph-svg" style={{ width: effWidth, height }} />
      {interactive && spec.sliders && spec.sliders.length > 0 && (
        <div className="mt-3 pt-3 border-t border-zinc-800 space-y-2">
          {spec.sliders.map((s) => (
            <label key={s.name} className="flex items-center gap-3 text-xs">
              <span className="font-mono text-zinc-300 w-8 shrink-0">{s.name}</span>
              <input
                type="range"
                min={s.min}
                max={s.max}
                step={s.step ?? (s.max - s.min) / 100}
                value={sliderValues[s.name] ?? s.init ?? (s.min + s.max) / 2}
                onChange={(e) => setSliderValues((v) => ({ ...v, [s.name]: parseFloat(e.target.value) }))}
                className="flex-1 accent-indigo-400"
              />
              <span className="font-mono text-zinc-100 w-16 text-right tabular-nums">
                {(sliderValues[s.name] ?? s.init ?? (s.min + s.max) / 2).toFixed(2).replace(/\.?0+$/, '')}
              </span>
            </label>
          ))}
        </div>
      )}
      {(resolvedFns.length > 0 || (spec.points && spec.points.length > 0)) && (
        <ul className="flex flex-wrap gap-x-4 gap-y-1.5 mt-2.5 pt-2 border-t border-zinc-800">
          {resolvedFns.map((f, i) => (
            <li key={i} className="flex items-center gap-2">
              <span
                className="inline-block rounded-sm"
                style={{ background: f.color, width: 18, height: 3 }}
              />
              <MathishText text={f.label!} auto className="text-[12px] text-zinc-100 leading-none" />
            </li>
          ))}
          {spec.points && spec.points.length > 0 && (
            <li className="flex items-center gap-2">
              <span className="inline-block rounded-full" style={{ background: '#f43f5e', width: 8, height: 8 }} />
              <MathishText text={spec.pointsLabel ?? `점 ${spec.points.length}개`} className="text-[12px] text-zinc-100 leading-none" />
            </li>
          )}
        </ul>
      )}
    </div>
  );
}

function SvgGraph({ svg, width = 360, height = 220 }: { svg: string; width?: number; height?: number }) {
  const [html, setHtml] = useState<string>('');
  useEffect(() => {
    let cancelled = false;
    loadDOMPurify().then((p) => {
      if (cancelled) return;
      setHtml(ensureSvgDimensions(sanitizeSvg(svg, p), width, height));
    });
    return () => { cancelled = true; };
  }, [svg, width, height]);

  return (
    <div
      className="graph-host bg-zinc-950 border border-zinc-700 rounded p-1 inline-block"
      style={{ maxWidth: width, maxHeight: height }}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}

export default function Graph(props: GraphProps) {
  const { kind, spec, svg, width, height, onOpen, interactive, hideCaption, noBroadcast } = props;
  const clickable = !interactive && onOpen;

  // Mirror to the sticky panel — unless we ARE the sticky panel (noBroadcast).
  // Without the guard, navigating to an older entry re-mounts this with
  // that entry's spec and the broadcast re-pushes it as a new latest,
  // bouncing the user back to the newest item.
  useEffect(() => {
    if (noBroadcast || interactive) return;
    if (kind === 'plot' && spec) broadcastLatestGraph({ kind, spec });
    else if (kind === 'svg' && svg) broadcastLatestGraph({ kind, svg });
  }, [kind, spec, svg, noBroadcast, interactive]);

  const content = kind === 'plot' && spec
    ? <PlotGraph spec={spec} width={width} height={height} interactive={interactive} hideCaption={hideCaption} />
    : kind === 'svg' && svg
      ? <SvgGraph svg={svg} width={width} height={height} />
      : <pre className="text-xs text-rose-300">invalid graph block</pre>;

  if (clickable) {
    return (
      <button
        type="button"
        onClick={onOpen}
        title="클릭하면 크게 봐요"
        className="block hover:ring-2 hover:ring-indigo-400/60 rounded transition"
      >{content}</button>
    );
  }
  return content;
}

// -------------------------------------------------------------- Modal

export function GraphModal({ open, kind, spec, svg, geomSpec, geom3dSpec, numberlineSpec, chartSpec, interactiveSpec, onClose }: {
  open: boolean; kind: 'plot' | 'svg' | 'geom' | 'geom3d' | 'numberline' | 'chart' | 'interactive';
  spec?: PlotSpec; svg?: string;
  geomSpec?: GeomSpec; geom3dSpec?: Geom3DSpec; numberlineSpec?: NumberlineSpec; chartSpec?: ChartSpec;
  interactiveSpec?: InteractiveSpec;
  onClose: () => void;
}) {
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [open, onClose]);

  if (!open) return null;
  const title =
    kind === 'geom'        ? (geomSpec?.title ?? '도형') :
    kind === 'geom3d'      ? (geom3dSpec?.title ?? '입체 도형') :
    kind === 'numberline'  ? (numberlineSpec?.title ?? '수직선') :
    kind === 'chart'       ? (chartSpec?.title ?? '차트') :
    kind === 'interactive' ? (interactiveSpec?.title ?? '탐구') :
                             (spec?.title ?? '그래프');
  return (
    <div
      className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4"
      onClick={onClose}
    >
      <div className={`bg-zinc-900 border border-zinc-700 rounded-xl shadow-2xl ${
             kind === 'geom3d' ? 'max-w-[min(1400px,95vw)] w-[min(1400px,95vw)]' : 'max-w-[min(820px,95vw)]'
           }`}
           onClick={(e) => e.stopPropagation()}>
        <header className="flex items-start justify-between gap-3 px-5 pt-4 pb-3 border-b border-zinc-800">
          <div className="flex-1 min-w-0"><Caption text={title} large /></div>
          <button onClick={onClose}
                  className="text-xs px-2 py-1 rounded border border-zinc-700 text-zinc-300 hover:bg-zinc-800 hover:text-zinc-100 shrink-0">
            닫기 (Esc)
          </button>
        </header>
        <div className="p-4">
          {kind === 'geom' && geomSpec ? (
            <Geometry spec={geomSpec} width={720} height={560} interactive hideCaption />
          ) : kind === 'geom3d' && geom3dSpec ? (
            <Geometry3D spec={geom3dSpec} width={1400} height={'min(820px, 78vh)'} hideCaption interactive />
          ) : kind === 'numberline' && numberlineSpec ? (
            <Numberline spec={numberlineSpec} width={720} interactive hideCaption />
          ) : kind === 'chart' && chartSpec ? (
            <StatsChart spec={chartSpec} width={720} height={460} interactive hideCaption />
          ) : kind === 'interactive' && interactiveSpec ? (
            <Interactive spec={interactiveSpec} width={720} height={480} interactive hideCaption />
          ) : (
            <Graph kind={kind as 'plot' | 'svg'} spec={spec} svg={svg} width={720} height={460} interactive hideCaption />
          )}
        </div>
      </div>
    </div>
  );
}

// -------------------------------------------------------------- Sticky side panel

const OPEN_KEY = 'math-study:graph-panel-open';
const RECT_KEY = 'math-study:graph-panel-rect';
const PANEL_MIN_W = 220;
const PANEL_MAX_W = 900;

// Natural aspect (width / height) for each content kind. Used to derive the
// graphic's height from the panel's width — the panel then auto-fits its
// own height to that content, so there's no dead space and no scrolling.
const CONTENT_ASPECT: Record<string, number> = {
  plot:  1.6,
  svg:   1.6,
  geom:  1.2,
  geom3d: 1.0,  // 정육면체 등 3D 도형은 정사각형이 자연
  chart: 1.5,
  // interactive 은 도형 + 슬라이더 패널 + readout 그리드를 다 가지므로
  // 같은 너비에서 더 길쭉. 1.0 = 정사각형 정도가 자연.
  interactive: 1.0,
};

// Panel rect stores position + width only. Height is content-driven (auto).
type PanelRect = { x: number; y: number; w: number };

// 좌표를 현재 viewport 안으로 강제. minVisibleX/Y는 panel이 100% 화면 밖으로
// 빠지지 않게 보장하는 최소 표시 면적 — panel header를 다시 잡을 수 있도록.
const MIN_VISIBLE_X = 120;   // header drag handle + 좌측 nav 버튼 묶음
const MIN_VISIBLE_Y = 32;    // header bar 한 줄

function clampRect(r: PanelRect, vw: number, vh: number): PanelRect {
  const w = Math.max(PANEL_MIN_W, Math.min(r.w, vw - 16));
  // x: 우측으로 너무 가면 panel 우측이 화면 밖, 좌측으로 너무 가면 panel header가 화면 밖.
  const x = Math.max(MIN_VISIBLE_X - w, Math.min(r.x, vw - MIN_VISIBLE_X));
  const y = Math.max(0, Math.min(r.y, vh - MIN_VISIBLE_Y));
  return { x, y, w };
}

function loadRect(): PanelRect {
  const vw = typeof window !== 'undefined' ? window.innerWidth : 1280;
  const vh = typeof window !== 'undefined' ? window.innerHeight : 800;
  const fallback: PanelRect = { x: Math.max(0, vw - 316), y: 80, w: Math.min(300, vw - 16) };
  try {
    const raw = window.localStorage.getItem(RECT_KEY);
    if (raw) {
      const r = JSON.parse(raw) as PanelRect & { h?: number };
      if (typeof r.x === 'number' && typeof r.y === 'number' && typeof r.w === 'number') {
        return clampRect(r, vw, vh);
      }
    }
  } catch { /* ignore */ }
  return clampRect(fallback, vw, vh);
}
function saveRect(r: PanelRect) {
  try { window.localStorage.setItem(RECT_KEY, JSON.stringify(r)); } catch { /* ignore */ }
}

export function StickyGraphPanel() {
  const [history, setHistory] = useState<GraphHistoryEntry[]>([]);
  const [idx, setIdx] = useState<number>(-1);            // index into history; -1 = none yet
  const [open, setOpen] = useState<boolean>(() => {
    try { return window.localStorage.getItem(OPEN_KEY) !== '0'; } catch { return true; }
  });
  const [modalOpen, setModalOpen] = useState(false);
  const [rect, setRect] = useState<PanelRect>(() => loadRect());

  const panelRef = useRef<HTMLDivElement | null>(null);
  // Drag / resize state — kept in a ref to avoid re-renders during pointer moves.
  const dragRef = useRef<
    | { kind: 'drag' | 'resize'; sx: number; sy: number; orig: PanelRect }
    | null
  >(null);

  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      const d = dragRef.current;
      if (!d) return;
      e.preventDefault();
      const dx = e.clientX - d.sx;
      const dy = e.clientY - d.sy;
      if (d.kind === 'drag') {
        // clampRect와 동일한 minimum visible 면적 보호.
        const clamped = clampRect(
          { x: d.orig.x + dx, y: d.orig.y + dy, w: d.orig.w },
          window.innerWidth, window.innerHeight,
        );
        setRect((r) => ({ ...r, x: clamped.x, y: clamped.y }));
      } else {
        // Width only. Height is content-driven: the graphic height comes
        // from natural aspect (CONTENT_ASPECT) and the panel auto-fits
        // around it. This means no dead space, no scrolling, and resize
        // implicitly maintains the content's natural ratio. We use the
        // larger absolute delta so dragging mostly horizontally OR mostly
        // vertically both feel right.
        const drive = Math.abs(dx) >= Math.abs(dy) ? dx : dy;
        const w = Math.max(PANEL_MIN_W, Math.min(PANEL_MAX_W, d.orig.w + drive));
        setRect((r) => ({ ...r, w }));
      }
    };
    const onUp = () => {
      if (dragRef.current) {
        dragRef.current = null;
        setRect((r) => { saveRect(r); return r; });
      }
    };
    window.addEventListener('mousemove', onMove);
    window.addEventListener('mouseup', onUp);
    return () => {
      window.removeEventListener('mousemove', onMove);
      window.removeEventListener('mouseup', onUp);
    };
  }, []);

  const startDrag = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    dragRef.current = { kind: 'drag', sx: e.clientX, sy: e.clientY, orig: rect };
  }, [rect]);
  const startResize = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    dragRef.current = { kind: 'resize', sx: e.clientX, sy: e.clientY, orig: rect };
  }, [rect]);
  // Stops the header's drag handler from firing when a button is clicked.
  const stopDrag = useCallback((e: React.MouseEvent) => { e.stopPropagation(); }, []);

  // Initial load + subscribe to broadcasts.
  useEffect(() => {
    const h = loadHistory();
    setHistory(h);
    setIdx(h.length - 1);
    const onGraph = (e: CustomEvent<GraphHistoryEntry>) => {
      // Reload from storage (storage already deduped + capped).
      const next = loadHistory();
      setHistory(next);
      setIdx(next.length - 1);          // jump to newest on new graph
    };
    window.addEventListener('math-study:graph', onGraph as EventListener);
    return () => window.removeEventListener('math-study:graph', onGraph as EventListener);
  }, []);

  // Persist open/closed across page nav.
  useEffect(() => {
    try { window.localStorage.setItem(OPEN_KEY, open ? '1' : '0'); } catch { /* ignore */ }
  }, [open]);

  // Window resize 안전장치: viewport가 줄어들면 panel rect를 화면 안으로 자동 보정.
  // 새로 들어온 rect가 이전과 동일하면 setState skip (불필요한 re-render 방지).
  useEffect(() => {
    const onResize = () => {
      setRect((r) => {
        const next = clampRect(r, window.innerWidth, window.innerHeight);
        if (next.x === r.x && next.y === r.y && next.w === r.w) return r;
        saveRect(next);
        return next;
      });
    };
    window.addEventListener('resize', onResize);
    return () => window.removeEventListener('resize', onResize);
  }, []);

  const total = history.length;
  const safeIdx = total > 0 ? Math.min(Math.max(idx, 0), total - 1) : -1;
  const current = safeIdx >= 0 ? history[safeIdx] : null;

  const fmtTime = (ts: number) => {
    const d = new Date(ts);
    const now = new Date();
    const sameDay = d.toDateString() === now.toDateString();
    return sameDay
      ? d.toLocaleTimeString('ko', { hour: '2-digit', minute: '2-digit' })
      : d.toLocaleDateString('ko', { month: 'short', day: 'numeric' });
  };

  const clearHistory = () => {
    if (!confirm('최근 그래프 기록을 모두 지울까요?')) return;
    try { window.localStorage.removeItem(HISTORY_KEY); } catch { /* ignore */ }
    setHistory([]); setIdx(-1);
  };

  if (!current) return null;

  // Pixel sizing for the inner graphic. Width = panel - inner padding.
  // Height = width / natural aspect (per content kind). Numberline is 1D
  // and uses its own natural height regardless of width.
  const INNER_PAD = 12;
  const graphicW = Math.max(PANEL_MIN_W - INNER_PAD, rect.w - INNER_PAD);
  const aspect = CONTENT_ASPECT[current.kind] ?? 1.5;
  const graphicH = current.kind === 'numberline' ? undefined : Math.round(graphicW / aspect);

  return (
    <>
      <aside
        className="block fixed z-30"
        style={{
          left: open ? rect.x : undefined,
          right: open ? undefined : 0,
          top: open ? rect.y : 80,
          width: open ? rect.w : 40,
        }}
      >
        {open ? (
          <div ref={panelRef}
               className="bg-zinc-900/95 backdrop-blur border border-zinc-700 rounded-lg shadow-xl overflow-hidden relative flex flex-col">
            <header
              onMouseDown={startDrag}
              className="flex items-center justify-between px-2 py-1.5 border-b border-zinc-800 bg-zinc-950/60 gap-1 cursor-move select-none"
              title="헤더를 드래그해 이동"
            >
              <div className="flex items-center gap-1 min-w-0">
                <button
                  onMouseDown={stopDrag}
                  onClick={() => setIdx((i) => Math.max(0, i - 1))}
                  disabled={safeIdx <= 0}
                  className="w-6 h-6 inline-flex items-center justify-center rounded text-zinc-400 hover:bg-zinc-800 hover:text-zinc-100 disabled:opacity-30"
                  title="이전 그래프"
                >←</button>
                <span className="text-[10px] text-zinc-500 tabular-nums whitespace-nowrap">
                  {safeIdx + 1} / {total}
                </span>
                <button
                  onMouseDown={stopDrag}
                  onClick={() => setIdx((i) => Math.min(total - 1, i + 1))}
                  disabled={safeIdx >= total - 1}
                  className="w-6 h-6 inline-flex items-center justify-center rounded text-zinc-400 hover:bg-zinc-800 hover:text-zinc-100 disabled:opacity-30"
                  title="다음 그래프"
                >→</button>
                <span className="text-[10px] text-zinc-500 ml-1 truncate">
                  {fmtTime(current.ts)}
                </span>
              </div>
              <div className="flex gap-0.5 shrink-0">
                <button onMouseDown={stopDrag}
                        onClick={() => {
                          setModalOpen(true);
                          if (current.kind === 'geom3d') {
                            window.dispatchEvent(new CustomEvent('math-study:geom3d-modal', { detail: { open: true } }));
                          }
                        }} title="확대"
                        className="w-6 h-6 inline-flex items-center justify-center rounded text-zinc-400 hover:bg-zinc-800 hover:text-zinc-100">⤢</button>
                <button onMouseDown={stopDrag} onClick={clearHistory} title="기록 지우기"
                        className="w-6 h-6 inline-flex items-center justify-center rounded text-zinc-500 hover:bg-rose-500/20 hover:text-rose-300">×</button>
                <button onMouseDown={stopDrag} onClick={() => setOpen(false)} title="패널 접기"
                        className="w-6 h-6 inline-flex items-center justify-center rounded text-zinc-400 hover:bg-zinc-800 hover:text-zinc-100">→</button>
              </div>
            </header>
            <div className="p-1.5">
              {/* `interactive` enables in-panel interactivity (function-plot
                  zoom + sliders, etc.) and ALSO suppresses re-broadcast (so
                  navigating doesn't snap back to latest). */}
              {current.kind === 'geom' && current.geomSpec ? (
                <Geometry spec={current.geomSpec} width={graphicW} height={graphicH ?? 210} hideCaption interactive />
              ) : current.kind === 'geom3d' && current.geom3dSpec ? (
                <Geometry3D spec={current.geom3dSpec} width={graphicW} height={graphicH ?? 220} hideCaption interactive={!modalOpen} noBroadcast />
              ) : current.kind === 'numberline' && current.numberlineSpec ? (
                <Numberline spec={current.numberlineSpec} width={graphicW} hideCaption interactive />
              ) : current.kind === 'chart' && current.chartSpec ? (
                <StatsChart spec={current.chartSpec} width={graphicW} height={graphicH ?? 210} hideCaption interactive />
              ) : current.kind === 'interactive' && current.interactiveSpec ? (
                <Interactive spec={current.interactiveSpec} width={graphicW} height={graphicH ?? 220} hideCaption interactive />
              ) : (
                <Graph
                  kind={current.kind as 'plot' | 'svg'}
                  spec={current.spec}
                  svg={current.svg}
                  width={graphicW}
                  height={graphicH ?? 170}
                  interactive
                />
              )}
            </div>
            {/* resize handle (bottom-right corner) */}
            <div
              onMouseDown={startResize}
              className="absolute bottom-0 right-0 w-4 h-4 cursor-se-resize select-none flex items-end justify-end pr-0.5 pb-0.5 text-zinc-500 hover:text-indigo-400"
              title="우하단을 드래그해 크기 조절"
            >
              <svg width="10" height="10" viewBox="0 0 10 10" aria-hidden="true">
                <path d="M 9 1 L 1 9 M 9 5 L 5 9 M 9 9 L 9 9" stroke="currentColor" strokeWidth="1.2" fill="none" />
              </svg>
            </div>
          </div>
        ) : (
          <button onClick={() => setOpen(true)}
                  className="bg-zinc-900/95 border border-zinc-700 rounded-l-lg px-2 py-3 text-zinc-300 hover:bg-zinc-800 hover:text-zinc-100 relative"
                  title={`최근 그래프 (${total}개)`}>
            📈
            {total > 0 && (
              <span className="absolute -top-1.5 -right-1.5 bg-indigo-500 text-[9px] font-mono rounded-full w-4 h-4 flex items-center justify-center">
                {total}
              </span>
            )}
          </button>
        )}
      </aside>
      <GraphModal
        open={modalOpen}
        kind={current.kind}
        spec={current.spec}
        svg={current.svg}
        geomSpec={current.geomSpec}
        geom3dSpec={current.geom3dSpec}
        numberlineSpec={current.numberlineSpec}
        chartSpec={current.chartSpec}
        interactiveSpec={current.interactiveSpec}
        onClose={() => {
          setModalOpen(false);
          window.dispatchEvent(new CustomEvent('math-study:geom3d-modal', { detail: { open: false } }));
        }}
      />
    </>
  );
}
