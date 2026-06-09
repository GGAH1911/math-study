// Numberline — 1D 좌표 선 위 점/구간/부등식 해 시각화.
//
// Spec (parsed from ```numberline``` fenced JSON block):
//   {
//     "range": [-5, 5],
//     "marks": [
//       {"at": 2, "label": "$a$", "closed": true},
//       {"at": -1, "label": "$b$", "closed": false}
//     ],
//     "intervals": [
//       {"from": -1, "to": 2, "closed": [false, true], "color": "#a5b4fc", "label": "$-1<x\\le 2$"}
//     ],
//     "title": "$x$의 범위"
//   }
//
// - `marks[].closed`: solid dot vs open circle (≥ vs >).
// - `intervals[].closed`: [leftIsClosed, rightIsClosed]; -∞/+∞ end is marked
//   with an open arrow.

import { useEffect, useMemo, useRef, useState } from 'react';
import { MathishText } from '../lib/mathish';

export type NumberlineSpec = {
  range: [number, number];
  marks?: Array<{ at: number; label?: string; closed?: boolean; color?: string }>;
  intervals?: Array<{
    from: number;
    to: number;
    closed?: [boolean, boolean];
    color?: string;
    label?: string;
    offset?: number;     // visual offset (in stack rows) for overlapping intervals
  }>;
  title?: string;
};

function fmtNum(n: number): string {
  if (!Number.isFinite(n)) return n > 0 ? '∞' : '-∞';
  const s = Math.abs(n) >= 100 ? n.toFixed(0) : n.toFixed(2);
  return s.includes('.') ? s.replace(/\.?0+$/, '') : s;
}

// Numberline labels render as LaTeX by default — use the shared MathishText
// in `auto` mode so bare strings like "x" are treated as math.
const NumberlineLabel = ({ text }: { text: string }) => <MathishText text={text} auto />;

type NumberlineProps = {
  spec: NumberlineSpec;
  width?: number;
  height?: number;
  onOpen?: () => void;
  interactive?: boolean;       // modal — skips broadcast + makes non-clickable
  hideCaption?: boolean;
  noBroadcast?: boolean;       // sticky panel uses this to avoid nav re-broadcast loop
};

export default function Numberline({ spec, width = 420, height, onOpen, interactive, hideCaption, noBroadcast }: NumberlineProps) {
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

  // Mirror to the sticky side panel — same contract as Geometry.
  useEffect(() => {
    if (interactive || noBroadcast) return;
    import('./Graph').then((m) => m.broadcastLatestGraph({ kind: 'numberline', numberlineSpec: spec }));
  }, [spec, interactive, noBroadcast]);

  const intervalRows = useMemo(() => Math.max(1, ...(spec.intervals?.map((i) => (i.offset ?? 0) + 1) ?? [1])), [spec.intervals]);
  // Natural height = stacked intervals above + main line + mark labels below.
  // The mark labels sit at baseY + 22 so we reserve ~32 below.
  const naturalH = 32 + intervalRows * 28 + 32;
  // A 1D number line gains nothing from being stretched vertically — and
  // doing so pushes everything to the bottom (baseY = H - 22). So we cap
  // height to natural unless the caller is in interactive (modal) mode AND
  // is asking for a clearly different value.
  const H = interactive && height && height > naturalH ? height : naturalH;
  const PAD = 30;
  const W = effWidth;
  // 역순 range([5,-5]) 정규화 — 안 하면 tickStep span<0, 눈금 0개, 모든 점이
  // 한 점으로 클램프. 그리고 폭 0([c,c]) 은 분모 0 → xPx 0/0=NaN(모든 좌표 소실).
  let [a, b] = spec.range;
  if (a > b) [a, b] = [b, a];
  const denom = (b - a) || 1;
  const xPx = (v: number) => {
    const clamped = Math.max(a, Math.min(b, v));
    return PAD + (clamped - a) / denom * (W - 2 * PAD);
  };
  const baseY = H - 32;     // y of the main line — leave 32px below for mark labels

  const tickStep = (() => {
    const span = b - a;
    for (const c of [0.1, 0.2, 0.5, 1, 2, 5, 10]) if (c * 8 >= span) return c;
    return 20;
  })();

  const tickFontPx = Math.max(9, Math.min(16, Math.round(effWidth / 45)));
  // Tick marks
  const ticks: React.ReactNode[] = [];
  const minT = Math.ceil(a / tickStep) * tickStep;
  for (let v = minT; v <= b + 1e-9; v += tickStep) {
    const x = xPx(v);
    ticks.push(<line key={`t${v}`} x1={x} y1={baseY - 4} x2={x} y2={baseY + 4} stroke="#a1a1aa" strokeWidth={1} />);
    ticks.push(<text key={`tl${v}`} x={x} y={baseY + 16} fill="#a1a1aa" fontSize={tickFontPx} textAnchor="middle">{fmtNum(v)}</text>);
  }

  // Normalize ±∞: missing/null endpoint = open infinity in that direction.
  // (JSON.stringify(Infinity) → "null", so specs round-tripped through
  // localStorage lose the infinity signal without this fallback.)
  const normInf = (v: number | null | undefined, side: 'from' | 'to') =>
    v == null ? (side === 'from' ? -Infinity : Infinity) : v;

  // Intervals (drawn ABOVE the main line, one row per offset)
  const intEls: React.ReactNode[] = [];
  const intLabels: React.ReactNode[] = [];
  (spec.intervals ?? []).forEach((iv, i) => {
    const row = iv.offset ?? 0;
    const y = baseY - 12 - row * 24;
    const color = iv.color ?? '#a5b4fc';
    const from = normInf(iv.from, 'from');
    const to = normInf(iv.to, 'to');
    const x1 = xPx(from), x2 = xPx(to);
    intEls.push(<line key={`iv${i}`} x1={x1} y1={y} x2={x2} y2={y} stroke={color} strokeWidth={4} strokeLinecap="round" />);
    // Endpoint decorations. `dir` = 'left' (this is the `from` end of the
    // interval — arrow points left for -∞) or 'right' (this is the `to`
    // end — arrow points right for +∞).
    const drawEndpoint = (atX: number, isFinite: boolean, isClosed: boolean, dir: 'left' | 'right', key: string) => {
      if (!isFinite) {
        // Triangle apex on the infinity side: left arrow has apex at (atX-8, y),
        // right arrow has apex at (atX+8, y).
        const apexX = dir === 'left' ? atX - 8 : atX + 8;
        const baseX = dir === 'left' ? atX + 2 : atX - 2;
        intEls.push(<polygon key={key}
                             points={`${baseX},${y - 4} ${baseX},${y + 4} ${apexX},${y}`}
                             fill={color} />);
      } else if (isClosed) {
        intEls.push(<circle key={key} cx={atX} cy={y} r={5} fill={color} stroke="#fafafa" strokeWidth={1.5} />);
      } else {
        intEls.push(<circle key={key} cx={atX} cy={y} r={5} fill="#0a0a0a" stroke={color} strokeWidth={2} />);
      }
    };
    // `iv.closed ?? [true,true]` 만으로는 closed=[true] 처럼 원소 1개로 오면
    // closed[1]=undefined → 오른쪽 끝점이 (닫힘 의도인데) 조용히 열림. 각 원소를
    // 개별 기본값 처리.
    const c = iv.closed ?? [];
    const closedL = c[0] ?? true;
    const closedR = c[1] ?? true;
    drawEndpoint(x1, Number.isFinite(from), closedL, 'left', `iv${i}_a`);
    drawEndpoint(x2, Number.isFinite(to), closedR, 'right', `iv${i}_b`);
    if (iv.label) {
      intLabels.push(
        <div key={`il${i}`} className="geom-label" style={{ left: (x1 + x2) / 2, top: y - 22, transform: 'translateX(-50%)' }}>
          <NumberlineLabel text={iv.label} />
        </div>
      );
    }
  });

  // Marks (points on the main line)
  const markEls: React.ReactNode[] = [];
  const markLabels: React.ReactNode[] = [];
  (spec.marks ?? []).forEach((m, i) => {
    const x = xPx(m.at);
    const color = m.color ?? '#fb7185';
    markEls.push(m.closed === false
      ? <circle key={`m${i}`} cx={x} cy={baseY} r={5} fill="#0a0a0a" stroke={color} strokeWidth={2} />
      : <circle key={`m${i}`} cx={x} cy={baseY} r={5} fill={color} stroke="#fafafa" strokeWidth={1.5} />);
    if (m.label) {
      markLabels.push(
        <div key={`ml${i}`} className="geom-label" style={{ left: x, top: baseY + 22, transform: 'translateX(-50%)' }}>
          <NumberlineLabel text={m.label} />
        </div>
      );
    }
  });

  const labelFontPx = Math.max(11, Math.min(18, Math.round(effWidth / 40)));
  const canvas = (
    <div ref={wrapRef} className="graph-host bg-zinc-950 border border-zinc-700/80 rounded-lg shadow-inner max-w-full"
         style={{ padding: '10px 12px', ['--geom-label-size' as string]: `${labelFontPx}px` } as React.CSSProperties}>
      {!hideCaption && spec.title && (
        <div className="text-zinc-300 mb-1 px-1 break-keep" style={{ fontSize: labelFontPx + 1 }}>
          <NumberlineLabel text={spec.title} />
        </div>
      )}
      <div style={{ position: 'relative', width: W, height: H }}>
        <svg width={W} height={H} className="graph-svg">
          {/* main horizontal line with arrows on both sides */}
          <defs>
            <marker id="nl-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 0 0 L 10 5 L 0 10 z" fill="#fafafa" />
            </marker>
            <marker id="nl-arrow-r" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 0 L 10 5 L 0 10 z" fill="#fafafa" />
            </marker>
          </defs>
          <line x1={PAD - 14} y1={baseY} x2={W - PAD + 14} y2={baseY}
                stroke="#fafafa" strokeWidth={1.4}
                markerEnd="url(#nl-arrow)" markerStart="url(#nl-arrow-r)" />
          {ticks}
          {intEls}
          {markEls}
        </svg>
        {intLabels}
        {markLabels}
      </div>
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
