import { useEffect, useRef, useState } from 'react';

// 학습 경로 시각화 v2 — 갈래가 합류하는 세로 층상 DAG("잉크 노선도"의 분기·환승 진화형).
// 위=기초(여러 갈래) → 아래로 내려가며 합류 → 맨 아래 목표로 수렴. 실제 선수관계 엣지 사용.
// 층 건너뛰는 긴 엣지는 더미 경유점으로 라우팅(Sugiyama식) → 직선이 화면을 가로지르지 않고
// 한 층씩 흘러 교차가 크게 준다. 좌표는 결정적(Math.random 금지).

type Mastery = 'unknown' | 'learning' | 'proficient' | 'mastered';
export type PathNodeVM = {
  id: string; label: string; domain: string | null; grade: string | null;
  mastery: Mastery; isGoal: boolean; isFrontier: boolean; layer: number;
};
export type PathEdgeVM = { from: string; to: string };
type Props = {
  nodes: PathNodeVM[]; edges: PathEdgeVM[];
  totalPrereqs: number; donePrereqs: number; todoCount: number;
};

function bodyProps(m: Mastery, isGoal: boolean): Record<string, string | number> {
  if (isGoal) return { fill: 'var(--paper-page)', stroke: 'var(--color-accent)', strokeWidth: 3 };
  switch (m) {
    case 'learning': return { fill: 'var(--color-mastery-learning)', fillOpacity: 0.45, stroke: 'var(--color-mastery-learning)', strokeWidth: 2 };
    case 'proficient': return { fill: 'var(--color-mastery-proficient)', stroke: 'var(--color-mastery-proficient)', strokeWidth: 2 };
    case 'mastered': return { fill: 'var(--color-mastery-mastered)', stroke: 'var(--color-mastery-mastered)', strokeWidth: 2 };
    default: return { fill: 'var(--paper-page)', stroke: 'var(--paper-dim)', strokeWidth: 1.8, strokeDasharray: '3 3' };
  }
}
const cut = (s: string, n: number) => (s.length > n ? s.slice(0, n) + '…' : s);

// Catmull-Rom → cubic bezier 스무딩(결정적) — 더미 경유점들을 부드러운 곡선으로.
function smoothPath(pts: { x: number; y: number }[]): string {
  if (pts.length < 2) return pts.length ? `M ${pts[0].x} ${pts[0].y}` : '';
  let d = `M ${pts[0].x.toFixed(1)} ${pts[0].y.toFixed(1)}`;
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[i - 1] ?? pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] ?? p2;
    const c1x = p1.x + (p2.x - p0.x) / 6, c1y = p1.y + (p2.y - p0.y) / 6;
    const c2x = p2.x - (p3.x - p1.x) / 6, c2y = p2.y - (p3.y - p1.y) / 6;
    d += ` C ${c1x.toFixed(1)} ${c1y.toFixed(1)} ${c2x.toFixed(1)} ${c2y.toFixed(1)} ${p2.x.toFixed(1)} ${p2.y.toFixed(1)}`;
  }
  return d;
}

export default function MetroMap({ nodes, edges, totalPrereqs, donePrereqs, todoCount }: Props) {
  const wrapRef = useRef<HTMLDivElement | null>(null);
  const [cw, setCw] = useState(720);

  useEffect(() => {
    const el = wrapRef.current;
    if (!el) return;
    const measure = () => setCw(Math.max(280, el.clientWidth));
    measure();
    if (typeof ResizeObserver === 'undefined') return;
    const ro = new ResizeObserver(measure);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  const narrow = cw < 560;
  const R = narrow ? 10 : 13;
  const LAYER_GAP = narrow ? 94 : 108;
  const PAD_TOP = 44, PAD_BOTTOM = 66, PAD_X = narrow ? 24 : 36;
  const MIN_COL = narrow ? 86 : 118;

  const layerOf = new Map(nodes.map((n) => [n.id, n.layer]));
  const maxLayer = Math.max(0, ...nodes.map((n) => n.layer));

  // 층별 item(실노드 + 더미). 더미키 = `d:<edgeIdx>:<layer>`.
  const items = new Map<number, string[]>();
  for (let L = 0; L <= maxLayer; L++) items.set(L, []);
  for (const n of nodes) items.get(n.layer)!.push(n.id);

  const up = new Map<string, string[]>();   // item → 상위층 이웃
  const down = new Map<string, string[]>();  // item → 하위층 이웃
  const link = (a: string, b: string) => {
    (down.get(a) ?? down.set(a, []).get(a)!).push(b);
    (up.get(b) ?? up.set(b, []).get(b)!).push(a);
  };
  const chains: string[][] = []; // 엣지별 [from, dummy.., to] 렌더용
  edges.forEach((e, ei) => {
    const Lf = layerOf.get(e.from) ?? 0, Lt = layerOf.get(e.to) ?? 0;
    const chain = [e.from];
    let prev = e.from;
    for (let L = Lf + 1; L < Lt; L++) {
      const d = `d:${ei}:${L}`;
      items.get(L)!.push(d);
      link(prev, d); chain.push(d); prev = d;
    }
    link(prev, e.to); chain.push(e.to);
    chains.push(chain);
  });

  // barycenter 스윕(교차 최소화) — 더미 포함 모든 item 대상.
  const pos = new Map<string, number>();
  const setPos = (arr: string[]) => arr.forEach((k, i) => pos.set(k, (i + 0.5) / arr.length));
  for (const arr of items.values()) setPos(arr);
  const bary = (k: string, neigh: Map<string, string[]>) => {
    const ns = neigh.get(k) ?? [];
    return ns.length ? ns.reduce((s, x) => s + (pos.get(x) ?? 0.5), 0) / ns.length : (pos.get(k) ?? 0.5);
  };
  for (let s = 0; s < 6; s++) {
    const dwn = s % 2 === 0;
    const seq = Array.from({ length: maxLayer + 1 }, (_, i) => (dwn ? i : maxLayer - i));
    for (const L of seq) {
      if (dwn && L === 0) continue;
      if (!dwn && L === maxLayer) continue;
      const arr = items.get(L)!;
      if (arr.length < 2) continue;
      arr.sort((a, b) => bary(a, dwn ? up : down) - bary(b, dwn ? up : down));
      setPos(arr);
    }
  }

  const maxLen = Math.max(1, ...[...items.values()].map((a) => a.length));
  const W = Math.max(cw, maxLen * MIN_COL + 2 * PAD_X);
  const innerW = W - 2 * PAD_X;
  const H = PAD_TOP + maxLayer * LAYER_GAP + PAD_BOTTOM;
  const XY = new Map<string, { x: number; y: number }>();
  for (const [L, arr] of items) {
    arr.forEach((k, i) => XY.set(k, { x: PAD_X + ((i + 0.5) / arr.length) * innerW, y: PAD_TOP + L * LAYER_GAP }));
  }
  const colWidth = innerW / maxLen;

  const go = (id: string) => { window.location.href = `/concepts/${id}`; };
  const pct = totalPrereqs > 0 ? Math.round((donePrereqs / totalPrereqs) * 100) : 0;

  // 엣지 path: chain 의 좌표열을 스무딩. 양끝(실노드)은 원 가장자리에서 시작/끝나게 R 만큼 당김.
  const chainPath = (chain: string[]) => {
    const pts = chain.map((k) => ({ ...XY.get(k)! }));
    if (pts.length >= 2) { pts[0] = { ...pts[0], y: pts[0].y + R }; pts[pts.length - 1] = { ...pts[pts.length - 1], y: pts[pts.length - 1].y - R }; }
    return smoothPath(pts);
  };

  return (
    <div ref={wrapRef} className="metro-wrap">
      <div className="metro-head">
        <div className="atlas-gauge"><i style={{ width: `${Math.max(3, pct)}%` }} /></div>
        <p className="metro-cap font-hand">
          {donePrereqs > 0 ? `✓ ${donePrereqs}개 이수하고 출발 · ${todoCount}개 남음` : `${todoCount}개 학습하면 목표 도착`}
          <span className="metro-legend"> · <span style={{ color: 'var(--pen-green)' }}>● 지금 배울 수 있음</span> · ◌ 미습득 · ◎ 목표</span>
        </p>
      </div>

      <div className="metro-scroll">
        <svg className="metro-svg" width={W} height={H} viewBox={`0 0 ${W} ${H}`} role="list" aria-label="학습 경로 그래프">
          <g>
            {chains.map((chain, i) => (
              <path key={`e${i}`} className="metro-edge" d={chainPath(chain)} pathLength={1} />
            ))}
          </g>
          {nodes.map((n) => {
            const p = XY.get(n.id)!;
            const cutN = Math.max(4, Math.floor((colWidth - 8) / (narrow ? 11 : 12.5)));
            return (
              <g
                key={n.id}
                className="metro-node"
                style={{ transformOrigin: `${p.x}px ${p.y}px`, animationDelay: `${0.1 + n.layer * 0.08}s` }}
                role="listitem"
                tabIndex={0}
                aria-label={`${n.label} · ${n.grade ?? ''} ${n.domain ?? ''} · ${n.isGoal ? '목표' : n.isFrontier ? '지금 배울 수 있음' : '선행'}`}
                onClick={() => go(n.id)}
                onKeyDown={(ev) => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); go(n.id); } }}
              >
                <title>{n.label}</title>
                {n.isFrontier && (
                  <circle className="metro-frontier-halo" cx={p.x} cy={p.y} r={R + 6} fill="none" stroke="var(--pen-green)" strokeWidth={2.4} />
                )}
                {n.isGoal && (
                  <circle cx={p.x} cy={p.y} r={R * 1.5 + 5} fill="none" stroke="var(--atlas-gold)" strokeWidth={2.2} />
                )}
                <circle cx={p.x} cy={p.y} r={n.isGoal ? R * 1.5 : R} {...bodyProps(n.mastery, n.isGoal)} />
                {n.isGoal && (
                  <path className="metro-flag" d={`M ${p.x + R * 1.5 + 2} ${p.y - 4} l 0 -18 l 14 5 l -14 5`} />
                )}
                <text
                  className="metro-name font-hand"
                  x={p.x}
                  y={p.y + R + (narrow ? 14 : 16)}
                  textAnchor="middle"
                  style={{ fontSize: n.isGoal ? (narrow ? 16 : 19) : (narrow ? 13 : 14.5) }}
                >
                  {n.isGoal ? n.label : cut(n.label, cutN)}{n.isGoal ? ' ·목표' : ''}
                </text>
              </g>
            );
          })}
        </svg>
      </div>
    </div>
  );
}
