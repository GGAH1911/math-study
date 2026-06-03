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
  try { return _math.evaluate(s); } catch { return NaN; }
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
    xNode = _math.parse(s.x).compile() as typeof xNode;
    yNode = _math.parse(s.y).compile() as typeof yNode;
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
  | { type: 'text'; at: [number, number]; text: string; color?: string };

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
      case 'angle':
        xs.push(s.at[0], s.from[0], s.to[0]); ys.push(s.at[1], s.from[1], s.to[1]); break;
      case 'text':
        xs.push(s.at[0]); ys.push(s.at[1]); break;
    }
  }
  if (xs.length === 0) return { x: [-5, 5], y: [-5, 5] };
  const xMin = Math.min(...xs), xMax = Math.max(...xs);
  const yMin = Math.min(...ys), yMax = Math.max(...ys);
  // padding 25% — 점이 viewport 끝에 안 붙도록. min 0.5 라 한 점만 있는 케이스도 보임.
  const padX = Math.max((xMax - xMin) * 0.25, 0.5);
  const padY = Math.max((yMax - yMin) * 0.25, 0.5);
  return { x: [xMin - padX, xMax + padX], y: [yMin - padY, yMax + padY] };
}

function GeometryCanvas({ spec, width, height, hideCaption = false }: { spec: GeomSpec; width: number; height: number; hideCaption?: boolean }) {
  const wrapRef = useRef<HTMLDivElement | null>(null);
  const [effWidth, setEffWidth] = useState(width);

  useEffect(() => {
    const el = wrapRef.current;
    if (!el) return;
    // rAF-throttle + ≥1px change guard — prevents ResizeObserver feedback
    // loops from pegging the main thread (see Graph.tsx PlotGraph for detail).
    let raf = 0;
    const measure = () => {
      raf = 0;
      const pw = el.parentElement?.clientWidth ?? width;
      const target = Math.round(Math.min(width, Math.max(240, pw - 16)));
      setEffWidth((prev) => (Math.abs(prev - target) < 1 ? prev : target));
    };
    measure();
    const ro = new ResizeObserver(() => { if (!raf) raf = requestAnimationFrame(measure); });
    if (el.parentElement) ro.observe(el.parentElement);
    return () => { if (raf) cancelAnimationFrame(raf); ro.disconnect(); };
  }, [width]);

  const bounds = useMemo(() => {
    const auto = autoBounds(spec.shapes);
    // LLM 명시 range/yRange 가 auto 보다 작으면 union — 모든 점이 화면 안 보장.
    // 명시 안 했으면 auto 사용.
    const ux: [number, number] = spec.range
      ? [Math.min(spec.range[0], auto.x[0]), Math.max(spec.range[1], auto.x[1])]
      : auto.x;
    const uy: [number, number] = spec.yRange
      ? [Math.min(spec.yRange[0], auto.y[0]), Math.max(spec.yRange[1], auto.y[1])]
      : auto.y;
    return { x: ux, y: uy };
  }, [spec]);

  // Map math coords → pixel coords, equal-aspect scaling so shapes
  // don't get distorted.
  const W = effWidth, H = height;
  const PAD = 24;
  const xSpan = bounds.x[1] - bounds.x[0];
  const ySpan = bounds.y[1] - bounds.y[0];
  const scale = Math.min((W - 2 * PAD) / xSpan, (H - 2 * PAD) / ySpan);
  const cx = (W - scale * xSpan) / 2;
  const cy = (H - scale * ySpan) / 2;
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
  const labels: React.ReactNode[] = [];   // HTML labels overlaid on top of SVG

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
  for (const s of spec.shapes) {
    if (s.type === 'point' && s.label
        && Array.isArray(s.at) && typeof s.at[0] === 'number' && typeof s.at[1] === 'number'
        && Number.isFinite(s.at[0]) && Number.isFinite(s.at[1])) {
      claimedLabels.add(`${s.at[0].toFixed(2)},${s.at[1].toFixed(2)}|${s.label}`);
    }
  }

  // Shapes
  spec.shapes.forEach((s, i) => {
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
          const offX = (() => {
            if (dir.includes('E')) return 10;
            if (dir.includes('W')) return -10;
            return 0;
          })();
          const offY = (() => {
            if (dir.includes('N')) return -labelFontPx - 10;
            if (dir.includes('S')) return 10;
            return -labelFontPx / 2 - 2;
          })();
          const tx = dir.includes('W') ? -100 : (dir.includes('E') ? 0 : -50);
          labels.push(
            <div key={`pl${i}`} className="geom-label"
                 style={{ left: xPx(x) + offX, top: yPx(y) + offY,
                          transform: `translateX(${tx}%)` }}>
              <GeomLabel text={s.label} />
            </div>
          );
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
        if (s.labels) {
          s.labels.forEach((lab, vi) => {
            const v = s.vertices[vi]; if (!v) return;
            if (typeof v[0] !== 'number' || typeof v[1] !== 'number') return;
            // 같은 (좌표, 라벨) 의 point shape 이 이미 라벨 그렸으면 skip — 중복 방지
            const key = `${v[0].toFixed(2)},${v[1].toFixed(2)}|${lab}`;
            if (claimedLabels.has(key)) return;
            claimedLabels.add(key);
            labels.push(
              <div key={`pgl${i}_${vi}`} className="geom-label"
                   style={{ left: xPx(v[0]) + 6, top: yPx(v[1]) - 14 }}>
                <GeomLabel text={lab} />
              </div>
            );
            els.push(<circle key={`pgv${i}_${vi}`} cx={xPx(v[0])} cy={yPx(v[1])} r={3} fill="#fafafa" />);
          });
        }
        break;
      }
      case 'line': case 'segment': {
        els.push(<line key={`ln${i}`} x1={xPx(s.from[0])} y1={yPx(s.from[1])} x2={xPx(s.to[0])} y2={yPx(s.to[1])}
                       stroke={s.color ?? c0} strokeWidth={1.8} strokeDasharray={s.dashed ? '6 4' : undefined} />);
        if (s.label) {
          const mx = (s.from[0] + s.to[0]) / 2, my = (s.from[1] + s.to[1]) / 2;
          labels.push(
            <div key={`lnl${i}`} className="geom-label"
                 style={{ left: xPx(mx) + 6, top: yPx(my) - 10 }}>
              <GeomLabel text={s.label} />
            </div>
          );
        }
        break;
      }
      case 'circle': {
        els.push(<circle key={`ci${i}`} cx={xPx(s.center[0])} cy={yPx(s.center[1])} r={s.radius * scale}
                         fill={s.fill ?? 'none'} fillOpacity={s.fillOpacity ?? (s.fill ? 0.18 : 1)}
                         stroke={s.stroke ?? c0} strokeWidth={1.8} />);
        if (s.label) labels.push(
          <div key={`cil${i}`} className="geom-label"
               style={{ left: xPx(s.center[0]) + 4, top: yPx(s.center[1]) - 6 }}>
            <GeomLabel text={s.label} />
          </div>
        );
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
        if (s.label) labels.push(
          <div key={`ell${i}`} className="geom-label"
               style={{ left: xPx(s.center[0]) + 4, top: yPx(s.center[1] + ryRaw) + 4 }}>
            <GeomLabel text={s.label} />
          </div>
        );
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
        if (s.label) labels.push(
          <div key={`hyl${i}`} className="geom-label"
               style={{ left: xPx(cx0) + 4, top: yPx(cy0) + 8 }}>
            <GeomLabel text={s.label} />
          </div>
        );
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
        if (s.label) labels.push(
          <div key={`pal${i}`} className="geom-label"
               style={{ left: xPx(h) + 4, top: yPx(k) - 12 }}>
            <GeomLabel text={s.label} />
          </div>
        );
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
          labels.push(
            <div key={`pml${i}`} className="geom-label"
                 style={{ left: mx + 4, top: my - 12 }}>
              <GeomLabel text={s.label} />
            </div>,
          );
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
        if (s.label) {
          const mx = (s.from[0] + s.to[0]) / 2, my = (s.from[1] + s.to[1]) / 2;
          labels.push(
            <div key={`vecl${i}`} className="geom-label"
                 style={{ left: xPx(mx) + 8, top: yPx(my) - 12 }}>
              <GeomLabel text={s.label} />
            </div>
          );
        }
        break;
      }
      case 'angle': {
        const r = s.radius ?? 0.5;
        // Compute the two arm directions from `at`
        const ang = (p: [number, number]) => Math.atan2(p[1] - s.at[1], p[0] - s.at[0]);
        const a1 = ang(s.from), a2 = ang(s.to);
        const startX = s.at[0] + r * Math.cos(a1);
        const startY = s.at[1] + r * Math.sin(a1);
        const endX = s.at[0] + r * Math.cos(a2);
        const endY = s.at[1] + r * Math.sin(a2);
        // SVG arc
        const sweep = ((a2 - a1 + 2 * Math.PI) % (2 * Math.PI)) > Math.PI ? 1 : 0;
        const d = `M ${xPx(startX)} ${yPx(startY)} A ${r * scale} ${r * scale} 0 ${sweep} 0 ${xPx(endX)} ${yPx(endY)}`;
        els.push(<path key={`ag${i}`} d={d} fill="none" stroke={s.color ?? c0} strokeWidth={1.5} />);
        if (s.label) {
          const midA = (a1 + a2) / 2;
          const lx = s.at[0] + (r + 0.3) * Math.cos(midA);
          const ly = s.at[1] + (r + 0.3) * Math.sin(midA);
          labels.push(
            <div key={`agl${i}`} className="geom-label"
                 style={{ left: xPx(lx) - 6, top: yPx(ly) - 8 }}>
              <GeomLabel text={s.label} />
            </div>
          );
        }
        break;
      }
      case 'text': {
        labels.push(
          <div key={`tx${i}`} className="geom-label"
               style={{ left: xPx(s.at[0]) + 4, top: yPx(s.at[1]) - 8, color: s.color }}>
            <GeomLabel text={s.text} />
          </div>
        );
        break;
      }
    }
  });

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
        </svg>
        {labels}
      </div>
    </div>
  );
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
};

export default function Geometry({ spec, width = DEFAULT_WIDTH, height = DEFAULT_HEIGHT, onOpen, interactive, hideCaption, noBroadcast }: Props) {
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
  const node = <GeometryCanvas spec={spec} width={width} height={height} hideCaption={hideCaption} />;
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
