// StatsChart — 확률·통계 단원 시각화 모음.
//
// Spec (parsed from ```chart``` fenced block):
//
//   histogram:
//     {"kind":"histogram","bins":[[0,10,5],[10,20,12],[20,30,8]],
//      "xLabel":"점수","yLabel":"빈도","title":"수학 점수 분포"}
//
//   bar:
//     {"kind":"bar","data":[{"x":"A","y":5},{"x":"B","y":12}],"title":"..."}
//
//   line:
//     {"kind":"line","data":[{"x":1,"y":2},{"x":2,"y":4}],"title":"..."}
//
//   normal (정규분포 곡선 + 음영):
//     {"kind":"normal","mean":0,"std":1,"shaded":[-1,1],"title":"표준정규"}
//
//   box (박스플롯):
//     {"kind":"box","stats":{"min":1,"q1":3,"median":5,"q3":7,"max":10},
//      "title":"박스플롯"}
//
// All rendered to SVG with the same dark-theme + KaTeX-aware caption.

import { useEffect, useMemo, useRef, useState } from 'react';
import { MathishText } from '../lib/mathish';

export type ChartSpec =
  | { kind: 'histogram'; bins: Array<[number, number, number]>; xLabel?: string; yLabel?: string; title?: string }
  | { kind: 'bar'; data: Array<{ x: string | number; y: number }>; xLabel?: string; yLabel?: string; title?: string }
  | { kind: 'line'; data: Array<{ x: number; y: number }>; xLabel?: string; yLabel?: string; title?: string }
  | { kind: 'normal'; mean: number; std: number; shaded?: [number, number]; range?: [number, number]; title?: string }
  | { kind: 'box'; stats: { min: number; q1: number; median: number; q3: number; max: number }; outliers?: number[]; title?: string };

function fmtNum(n: number): string {
  if (!Number.isFinite(n)) return '?';
  const s = Math.abs(n) >= 100 ? n.toFixed(0) : n.toFixed(2);
  // Strip trailing zeros AFTER the decimal point only — never from
  // integers (the old `/\.?0+$/` collapsed "100" → "1").
  return s.includes('.') ? s.replace(/\.?0+$/, '') : s;
}

// Chart labels — titles are usually plain Korean text with optional `$...$`
// segments, so don't use `auto` mode (that would try to render the whole
// string as LaTeX, e.g. "수학 점수" → broken).
function ChartLabel({ text, large = false }: { text: string; large?: boolean }) {
  return <MathishText text={text}
                      className={large ? 'text-sm text-zinc-100 font-semibold' : 'text-[11px] text-zinc-300'} />;
}

const PAD = { l: 40, r: 16, t: 12, b: 32 };

// Shared axis title overlay. yLabel is rendered via translate-then-rotate
// so the rotation pivot doesn't push tail characters off-canvas (the prior
// rotate-around-(12,H/2) form clipped multi-char Korean labels like "점수").
function AxisTitles({ W, H, xLabel, yLabel }: { W: number; H: number; xLabel?: string; yLabel?: string }) {
  return (
    <>
      {xLabel && (
        <text x={PAD.l + (W - PAD.l - PAD.r) / 2} y={H - 4}
              fill="#d4d4d8" fontSize={11} textAnchor="middle">{xLabel}</text>
      )}
      {yLabel && (
        <g transform={`translate(11 ${PAD.t + (H - PAD.t - PAD.b) / 2}) rotate(-90)`}>
          <text fill="#d4d4d8" fontSize={11} textAnchor="middle">{yLabel}</text>
        </g>
      )}
    </>
  );
}

// Histogram + bar share the layout — bars vary, axes identical.
function BarLike({ width, height, bars, xLabels, yMax, xLabel, yLabel }: {
  width: number; height: number;
  bars: Array<{ x0: number; x1: number; h: number; color: string }>;
  xLabels: Array<{ x: number; text: string }>;
  yMax: number;
  xLabel?: string; yLabel?: string;
}) {
  const W = width, H = height;
  const plotW = W - PAD.l - PAD.r;
  const plotH = H - PAD.t - PAD.b;

  const yTicks = (() => {
    const out: number[] = [];
    const step = niceStep(yMax / 5);
    for (let v = 0; v <= yMax + 1e-9; v += step) out.push(v);
    return out;
  })();

  return (
    <svg width={W} height={H} className="graph-svg">
      {/* y grid + labels */}
      {yTicks.map((v) => {
        const y = PAD.t + plotH * (1 - v / yMax);
        return (
          <g key={`y${v}`}>
            <line x1={PAD.l} y1={y} x2={W - PAD.r} y2={y} stroke="#3f3f46" strokeWidth={0.5} opacity={0.6} />
            <text x={PAD.l - 6} y={y + 4} fill="#a1a1aa" fontSize={10} textAnchor="end">{fmtNum(v)}</text>
          </g>
        );
      })}
      {/* axes */}
      <line x1={PAD.l} y1={PAD.t} x2={PAD.l} y2={H - PAD.b} stroke="#fafafa" strokeWidth={1.4} />
      <line x1={PAD.l} y1={H - PAD.b} x2={W - PAD.r} y2={H - PAD.b} stroke="#fafafa" strokeWidth={1.4} />
      {/* bars */}
      {bars.map((b, i) => {
        const x = PAD.l + plotW * b.x0;
        const w = plotW * (b.x1 - b.x0);
        const h = plotH * (b.h / yMax);
        const y = PAD.t + plotH - h;
        return <rect key={i} x={x + 1} y={y} width={Math.max(2, w - 2)} height={h}
                     fill={b.color} stroke={b.color} strokeWidth={1} opacity={0.85} />;
      })}
      {/* x labels — pin anchor to start/end at the boundaries so the
          first/last label doesn't get half-clipped by the SVG viewport. */}
      {xLabels.map((l, i) => {
        const anchor = l.x <= 0.01 ? 'start' : l.x >= 0.99 ? 'end' : 'middle';
        return (
          <text key={`xl${i}`} x={PAD.l + plotW * l.x} y={H - PAD.b + 14} fill="#a1a1aa" fontSize={10} textAnchor={anchor}>
            {l.text}
          </text>
        );
      })}
      <AxisTitles W={W} H={H} xLabel={xLabel} yLabel={yLabel} />
    </svg>
  );
}

function niceStep(target: number): number {
  for (const c of [0.1, 0.2, 0.25, 0.5, 1, 2, 5, 10, 20, 25, 50, 100, 200, 500, 1000])
    if (c >= target) return c;
  return target;
}

function HistogramView({ spec, width, height }: { spec: Extract<ChartSpec, { kind: 'histogram' }>; width: number; height: number }) {
  const minX = Math.min(...spec.bins.map((b) => b[0]));
  const maxX = Math.max(...spec.bins.map((b) => b[1]));
  const yMax = Math.max(...spec.bins.map((b) => b[2])) * 1.1;
  const span = maxX - minX || 1;
  const bars = spec.bins.map((b) => ({
    x0: (b[0] - minX) / span,
    x1: (b[1] - minX) / span,
    h: b[2],
    color: '#a5b4fc',
  }));
  // x labels at bin edges
  const xLabels: Array<{ x: number; text: string }> = [];
  const seen = new Set<number>();
  for (const b of spec.bins) {
    for (const v of [b[0], b[1]]) {
      if (seen.has(v)) continue;
      seen.add(v);
      xLabels.push({ x: (v - minX) / span, text: fmtNum(v) });
    }
  }
  return <BarLike width={width} height={height} bars={bars} xLabels={xLabels}
                  yMax={yMax} xLabel={spec.xLabel} yLabel={spec.yLabel} />;
}

function BarView({ spec, width, height }: { spec: Extract<ChartSpec, { kind: 'bar' }>; width: number; height: number }) {
  const n = spec.data.length;
  const yMax = Math.max(...spec.data.map((d) => d.y)) * 1.15;
  const bars = spec.data.map((d, i) => ({
    x0: (i + 0.1) / n, x1: (i + 0.9) / n, h: d.y, color: '#a5b4fc',
  }));
  const xLabels = spec.data.map((d, i) => ({ x: (i + 0.5) / n, text: String(d.x) }));
  return <BarLike width={width} height={height} bars={bars} xLabels={xLabels}
                  yMax={yMax} xLabel={spec.xLabel} yLabel={spec.yLabel} />;
}

function LineView({ spec, width, height }: { spec: Extract<ChartSpec, { kind: 'line' }>; width: number; height: number }) {
  const W = width, H = height;
  const plotW = W - PAD.l - PAD.r;
  const plotH = H - PAD.t - PAD.b;
  const xs = spec.data.map((d) => d.x);
  const ys = spec.data.map((d) => d.y);
  const xMin = Math.min(...xs), xMax = Math.max(...xs);
  const yMin = Math.min(0, ...ys), yMax = Math.max(...ys) * 1.1;
  const ySpan = yMax - yMin || 1;
  const sx = (v: number) => PAD.l + plotW * (v - xMin) / (xMax - xMin || 1);
  const sy = (v: number) => PAD.t + plotH * (1 - (v - yMin) / ySpan);
  const d = spec.data.map((p, i) => `${i === 0 ? 'M' : 'L'} ${sx(p.x)} ${sy(p.y)}`).join(' ');

  // Y ticks
  const yStep = niceStep(ySpan / 5);
  const yTicks: number[] = [];
  for (let v = Math.ceil(yMin / yStep) * yStep; v <= yMax + 1e-9; v += yStep) yTicks.push(v);
  // X ticks — show all data x-values if small N, else 5 evenly spaced
  const xTicks: number[] = xs.length <= 8 ? xs.slice() : Array.from({ length: 5 }, (_, i) => xMin + (xMax - xMin) * i / 4);

  return (
    <svg width={W} height={H} className="graph-svg">
      {/* y grid + labels */}
      {yTicks.map((v) => {
        const y = sy(v);
        return (
          <g key={`y${v}`}>
            <line x1={PAD.l} y1={y} x2={W - PAD.r} y2={y} stroke="#3f3f46" strokeWidth={0.5} opacity={0.6} />
            <text x={PAD.l - 6} y={y + 4} fill="#a1a1aa" fontSize={10} textAnchor="end">{fmtNum(v)}</text>
          </g>
        );
      })}
      {/* axes */}
      <line x1={PAD.l} y1={PAD.t} x2={PAD.l} y2={H - PAD.b} stroke="#fafafa" strokeWidth={1.4} />
      <line x1={PAD.l} y1={H - PAD.b} x2={W - PAD.r} y2={H - PAD.b} stroke="#fafafa" strokeWidth={1.4} />
      {/* x ticks */}
      {xTicks.map((v, i) => (
        <g key={`x${i}`}>
          <line x1={sx(v)} y1={H - PAD.b} x2={sx(v)} y2={H - PAD.b + 4} stroke="#a1a1aa" strokeWidth={1} />
          <text x={sx(v)} y={H - PAD.b + 14} fill="#a1a1aa" fontSize={10} textAnchor="middle">{fmtNum(v)}</text>
        </g>
      ))}
      {/* line */}
      <path d={d} fill="none" stroke="#a5b4fc" strokeWidth={2.25} />
      {/* points */}
      {spec.data.map((p, i) => (
        <circle key={i} cx={sx(p.x)} cy={sy(p.y)} r={3} fill="#fb7185" />
      ))}
      <AxisTitles W={W} H={H} xLabel={spec.xLabel} yLabel={spec.yLabel} />
    </svg>
  );
}

function NormalView({ spec, width, height }: { spec: Extract<ChartSpec, { kind: 'normal' }>; width: number; height: number }) {
  const W = width, H = height;
  const plotW = W - PAD.l - PAD.r;
  const plotH = H - PAD.t - PAD.b;
  const { mean, std } = spec;
  const range = spec.range ?? [mean - 4 * std, mean + 4 * std];
  const pdf = (x: number) => (1 / (std * Math.sqrt(2 * Math.PI))) * Math.exp(-((x - mean) ** 2) / (2 * std * std));
  const N = 200;
  const samples: Array<[number, number]> = [];
  for (let i = 0; i <= N; i++) {
    const x = range[0] + (range[1] - range[0]) * (i / N);
    samples.push([x, pdf(x)]);
  }
  const yMax = pdf(mean) * 1.15;
  const sx = (v: number) => PAD.l + plotW * (v - range[0]) / (range[1] - range[0]);
  const sy = (v: number) => PAD.t + plotH * (1 - v / yMax);
  const curveD = samples.map((p, i) => `${i === 0 ? 'M' : 'L'} ${sx(p[0])} ${sy(p[1])}`).join(' ');

  let shadedD: string | null = null;
  if (spec.shaded) {
    const [a, b] = spec.shaded;
    const pts: Array<[number, number]> = [];
    for (let i = 0; i <= N; i++) {
      const x = a + (b - a) * (i / N);
      pts.push([x, pdf(x)]);
    }
    shadedD = `M ${sx(a)} ${sy(0)} ` + pts.map((p) => `L ${sx(p[0])} ${sy(p[1])}`).join(' ') + ` L ${sx(b)} ${sy(0)} Z`;
  }

  const xTicks: number[] = [];
  for (let k = -3; k <= 3; k++) xTicks.push(mean + k * std);

  return (
    <svg width={W} height={H} className="graph-svg">
      {/* baseline */}
      <line x1={PAD.l} y1={H - PAD.b} x2={W - PAD.r} y2={H - PAD.b} stroke="#fafafa" strokeWidth={1.4} />
      {/* shaded region */}
      {shadedD && <path d={shadedD} fill="rgba(165,180,252,0.35)" stroke="none" />}
      {/* curve */}
      <path d={curveD} fill="none" stroke="#a5b4fc" strokeWidth={2.25} />
      {/* mean line */}
      <line x1={sx(mean)} y1={PAD.t} x2={sx(mean)} y2={H - PAD.b}
            stroke="#fbbf24" strokeWidth={1} strokeDasharray="4 3" />
      {/* x ticks (μ±kσ) */}
      {xTicks.map((v, i) => {
        const k = i - 3;
        const label = k === 0 ? 'μ' : (k > 0 ? `μ+${k}σ` : `μ${k}σ`);
        return (
          <g key={i}>
            <line x1={sx(v)} y1={H - PAD.b} x2={sx(v)} y2={H - PAD.b + 4} stroke="#a1a1aa" strokeWidth={1} />
            <text x={sx(v)} y={H - PAD.b + 16} fill="#a1a1aa" fontSize={10} textAnchor="middle">{label}</text>
          </g>
        );
      })}
    </svg>
  );
}

function BoxView({ spec, width, height }: { spec: Extract<ChartSpec, { kind: 'box' }>; width: number; height: number }) {
  const W = width, H = height;
  const plotH = H - PAD.t - PAD.b;
  const { min, q1, median, q3, max } = spec.stats;
  const dataMin = Math.min(min, ...(spec.outliers ?? []));
  const dataMax = Math.max(max, ...(spec.outliers ?? []));
  const span = dataMax - dataMin || 1;
  const sx = (v: number) => PAD.l + (W - PAD.l - PAD.r) * (v - dataMin) / span;
  const boxY = PAD.t + plotH * 0.3;
  const boxH = plotH * 0.4;
  const midY = boxY + boxH / 2;

  return (
    <svg width={W} height={H} className="graph-svg">
      {/* axis baseline */}
      <line x1={PAD.l} y1={H - PAD.b} x2={W - PAD.r} y2={H - PAD.b} stroke="#fafafa" strokeWidth={1.4} />
      {/* whiskers */}
      <line x1={sx(min)} y1={midY} x2={sx(q1)} y2={midY} stroke="#fafafa" strokeWidth={1.5} />
      <line x1={sx(q3)} y1={midY} x2={sx(max)} y2={midY} stroke="#fafafa" strokeWidth={1.5} />
      <line x1={sx(min)} y1={boxY} x2={sx(min)} y2={boxY + boxH} stroke="#fafafa" strokeWidth={1.5} />
      <line x1={sx(max)} y1={boxY} x2={sx(max)} y2={boxY + boxH} stroke="#fafafa" strokeWidth={1.5} />
      {/* box */}
      <rect x={sx(q1)} y={boxY} width={sx(q3) - sx(q1)} height={boxH}
            fill="rgba(165,180,252,0.35)" stroke="#a5b4fc" strokeWidth={1.8} />
      {/* median */}
      <line x1={sx(median)} y1={boxY} x2={sx(median)} y2={boxY + boxH} stroke="#fbbf24" strokeWidth={2.5} />
      {/* outliers */}
      {(spec.outliers ?? []).map((v, i) => (
        <circle key={i} cx={sx(v)} cy={midY} r={3} fill="#fb7185" stroke="#fafafa" strokeWidth={1} />
      ))}
      {/* tick labels */}
      {[min, q1, median, q3, max].map((v, i) => (
        <g key={i}>
          <line x1={sx(v)} y1={H - PAD.b - 2} x2={sx(v)} y2={H - PAD.b + 4} stroke="#a1a1aa" strokeWidth={1} />
          <text x={sx(v)} y={H - PAD.b + 16} fill="#a1a1aa" fontSize={10} textAnchor="middle">{fmtNum(v)}</text>
        </g>
      ))}
    </svg>
  );
}

type StatsChartProps = {
  spec: ChartSpec;
  width?: number;
  height?: number;
  hideCaption?: boolean;
  onOpen?: () => void;
  interactive?: boolean;
  noBroadcast?: boolean;
};

export default function StatsChart({ spec, width = 420, height = 280, hideCaption = false, onOpen, interactive, noBroadcast }: StatsChartProps) {
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
      const target = Math.round(Math.min(width, Math.max(280, pw - 16)));
      setEffWidth((prev) => (Math.abs(prev - target) < 1 ? prev : target));
    };
    measure();
    const ro = new ResizeObserver(() => { if (!raf) raf = requestAnimationFrame(measure); });
    if (el.parentElement) ro.observe(el.parentElement);
    return () => { if (raf) cancelAnimationFrame(raf); ro.disconnect(); };
  }, [width]);

  // Mirror to the sticky side panel.
  useEffect(() => {
    if (interactive || noBroadcast) return;
    import('./Graph').then((m) => m.broadcastLatestGraph({ kind: 'chart', chartSpec: spec }));
  }, [spec, interactive, noBroadcast]);

  const node = useMemo(() => {
    switch (spec.kind) {
      case 'histogram': return <HistogramView spec={spec} width={effWidth} height={height} />;
      case 'bar':       return <BarView spec={spec} width={effWidth} height={height} />;
      case 'line':      return <LineView spec={spec} width={effWidth} height={height} />;
      case 'normal':    return <NormalView spec={spec} width={effWidth} height={height} />;
      case 'box':       return <BoxView spec={spec} width={effWidth} height={height} />;
      default:          return <pre className="text-xs text-rose-300">unknown chart kind</pre>;
    }
  }, [spec, effWidth, height]);

  const canvas = (
    <div ref={wrapRef} className="graph-host bg-zinc-950 border border-zinc-700/80 rounded-lg shadow-inner max-w-full"
         style={{ padding: '10px 12px' }}>
      {!hideCaption && spec.title && (
        <div className="mb-1 px-1 break-keep"><ChartLabel text={spec.title} /></div>
      )}
      {node}
    </div>
  );

  if (!interactive && onOpen) {
    return (
      <button type="button" onClick={onOpen} title="클릭하면 크게 봐요"
              className="block hover:ring-2 hover:ring-indigo-400/60 rounded-lg transition">
        {canvas}
      </button>
    );
  }
  return canvas;
}
