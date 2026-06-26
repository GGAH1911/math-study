import { useEffect, useRef, useState } from 'react';
import { hasWidget } from '../lib/concept-widgets';

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
// 라벨 줄바꿈 — 잘라내지 않고(…금지) maxChars 폭에 맞춰 단어 단위로 최대 3줄.
function wrapLabel(label: string, maxChars: number): string[] {
  const words = label.split(/\s+/).filter(Boolean);
  const lines: string[] = [];
  let cur = '';
  for (const w of words) {
    if (!cur) cur = w;
    else if ((cur + ' ' + w).length <= maxChars) cur += ' ' + w;
    else { lines.push(cur); cur = w; }
  }
  if (cur) lines.push(cur);
  // 한 단어가 폭을 넘으면(공백 없는 긴 개념명) 글자 단위로 강제 분할.
  const out: string[] = [];
  for (const l of lines) {
    if (l.length <= maxChars) out.push(l);
    else for (let i = 0; i < l.length; i += maxChars) out.push(l.slice(i, i + maxChars));
  }
  return out.slice(0, 3);
}

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
  const R = narrow ? 11 : 14;
  const LAYER_GAP = narrow ? 112 : 132; // 라벨 줄바꿈(최대 3줄) + 큰 폰트 여유
  const PAD_TOP = 46, PAD_BOTTOM = 82, PAD_X = narrow ? 26 : 40;
  const MIN_COL = narrow ? 96 : 132;
  const NAME_FS = narrow ? 14 : 16.5;   // 키운 라벨 폰트
  const GOAL_FS = narrow ? 17 : 21;

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
  // 자연 좌표폭: 노드가 편한 간격(MIN_COL)을 갖는 폭. 컨테이너보다 좁으면 컨테이너에 맞춤(확대 방지).
  // SVG 는 viewBox=naturalW + width:100% 로 컨테이너에 *맞춰 스케일* → 가로 오버플로우 없음.
  // 작은 경로 = 1:1 정상, 빽빽한 경로 = 통째로 축소(노드·라벨 비율 유지, 겹침 없이 작아짐).
  const naturalW = Math.max(cw, maxLen * MIN_COL + 2 * PAD_X);
  const innerW = naturalW - 2 * PAD_X;
  const H = PAD_TOP + maxLayer * LAYER_GAP + PAD_BOTTOM;
  const XY = new Map<string, { x: number; y: number }>();
  for (const [L, arr] of items) {
    arr.forEach((k, i) => XY.set(k, { x: PAD_X + ((i + 0.5) / arr.length) * innerW, y: PAD_TOP + L * LAYER_GAP }));
  }

  const go = (id: string) => { window.location.href = `/concepts/${id}`; };
  const pct = totalPrereqs > 0 ? Math.round((donePrereqs / totalPrereqs) * 100) : 0;

  // 엣지 path: chain 좌표열 스무딩. 양끝(실노드)은 *중앙을 향해* 이웃 방향으로 R 만큼 당겨
  // 원 가장자리에서 시작/끝나게 한다 → 선이 원 중앙을 가리키는 방사형(상/하단 stub 아님).
  const trimToward = (p: { x: number; y: number }, t: { x: number; y: number }, d: number) => {
    const dx = t.x - p.x, dy = t.y - p.y, len = Math.hypot(dx, dy) || 1;
    return { x: p.x + (dx / len) * d, y: p.y + (dy / len) * d };
  };
  const chainPath = (chain: string[]) => {
    const pts = chain.map((k) => ({ ...XY.get(k)! }));
    if (pts.length >= 2) {
      pts[0] = trimToward(pts[0], pts[1], R);
      pts[pts.length - 1] = trimToward(pts[pts.length - 1], pts[pts.length - 2], R);
    }
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
        <svg
          className="metro-svg"
          viewBox={`0 0 ${naturalW} ${H}`}
          preserveAspectRatio="xMidYMin meet"
          style={{ width: '100%', height: 'auto' }}
          role="list"
          aria-label="학습 경로 그래프"
        >
          <g>
            {chains.map((chain, i) => (
              <path key={`e${i}`} className="metro-edge" d={chainPath(chain)} pathLength={1} />
            ))}
          </g>
          {nodes.map((n) => {
            const p = XY.get(n.id)!;
            const fs = n.isGoal ? GOAL_FS : NAME_FS;
            const availW = innerW / (items.get(n.layer)?.length ?? 1); // 그 층의 노드 간격(더미 포함)
            const maxChars = Math.max(5, Math.floor((availW - 6) / fs));
            const lines = wrapLabel(n.isGoal ? `${n.label} ·목표` : n.label, maxChars);
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
                {hasWidget(n.id) && (
                  <text
                    x={p.x + (n.isGoal ? R * 1.5 : R) - 1}
                    y={p.y - (n.isGoal ? R * 1.5 : R) + 3}
                    fontSize={11}
                    textAnchor="middle"
                    fill="var(--color-accent)"
                    aria-hidden="true"
                  >🔭</text>
                )}
                {n.isGoal && (
                  <path className="metro-flag" d={`M ${p.x + R * 1.5 + 2} ${p.y - 4} l 0 -18 l 14 5 l -14 5`} />
                )}
                <text
                  className="metro-name font-hand"
                  x={p.x}
                  y={p.y + R + fs}
                  textAnchor="middle"
                  style={{ fontSize: fs }}
                >
                  {lines.map((ln, i) => (
                    <tspan key={i} x={p.x} dy={i === 0 ? 0 : fs * 1.02}>{ln}</tspan>
                  ))}
                </text>
              </g>
            );
          })}
        </svg>
      </div>
    </div>
  );
}
