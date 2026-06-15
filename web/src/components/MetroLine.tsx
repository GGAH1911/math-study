import { useEffect, useRef, useState } from 'react';

// 학습 경로 시각화 — "만년필로 그어 내려간 한 줄기 잉크 노선".
// buildLearningPath 의 steps[](위상정렬: 선행→목표)를 세로 스파인 노선도로 그린다.
// 디자인 계약은 web/src/styles/global.css 의 .metro-* 블록 + 토큰 var() 직바인딩.
// 모든 좌표는 결정적(Math.random 금지) — prerender=false SSR 매 요청 동일해야 함.

type Mastery = 'unknown' | 'learning' | 'proficient' | 'mastered';

export type PathStepVM = {
  id: string;
  label: string;
  domain: string | null;
  grade: string | null;
  mastery: Mastery;
  isGoal: boolean;
};

type Props = {
  steps: PathStepVM[];
  goal: { id: string; label: string };
  totalPrereqs: number;
  donePrereqs: number;
  todoCount: number;
};

const MASTERY_KO: Record<Mastery, string> = {
  unknown: '미습득', learning: '학습중', proficient: '능숙', mastered: '숙달',
};
const MASTERY_VAR: Record<Mastery, string> = {
  unknown: 'var(--ink-faint)', // 미습득은 경고색 대신 중립(빨강 과다 방지)
  learning: 'var(--color-mastery-learning)',
  proficient: 'var(--color-mastery-proficient)',
  mastered: 'var(--color-mastery-mastered)',
};

// 노드 본체 채움/윤곽 — mastery·목표별. (mastery 4색 환상 주의: 실제 steps 는
// 거의 unknown/learning + 목표 1개라 unknown 은 중립 점선, 강조는 frontier/목표에.)
function bodyProps(m: Mastery, isGoal: boolean): Record<string, string | number> {
  if (isGoal) {
    return { fill: 'var(--paper-page)', stroke: 'var(--color-accent)', strokeWidth: 3 };
  }
  switch (m) {
    case 'learning':
      return { fill: 'var(--color-mastery-learning)', fillOpacity: 0.45, stroke: 'var(--color-mastery-learning)', strokeWidth: 2 };
    case 'proficient':
      return { fill: 'var(--color-mastery-proficient)', stroke: 'var(--color-mastery-proficient)', strokeWidth: 2 };
    case 'mastered':
      return { fill: 'var(--color-mastery-mastered)', stroke: 'var(--color-mastery-mastered)', strokeWidth: 2 };
    default: // unknown — 중립 점선 윤곽, 빈 종이 채움
      return { fill: 'var(--paper-page)', stroke: 'var(--paper-dim)', strokeWidth: 1.8, strokeDasharray: '3 3' };
  }
}

// 결정적 wobble: 노드 사이 중간점에만 미세 가로 흔들림(노드 자신은 SPINE_X 고정 →
// 스파인이 모든 역 중심을 정확히 통과). amp ~ ±3px.
function wobble(k: number, amp: number): number {
  return (((k * 131) % 9) - 4) / 4 * amp;
}

// Catmull-Rom → cubic bezier 스무딩(결정적). 점들을 부드러운 곡선으로 잇는다.
function smoothPath(pts: { x: number; y: number }[]): string {
  if (pts.length < 2) return pts.length ? `M ${pts[0].x} ${pts[0].y}` : '';
  let d = `M ${pts[0].x.toFixed(2)} ${pts[0].y.toFixed(2)}`;
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[i - 1] ?? pts[i];
    const p1 = pts[i];
    const p2 = pts[i + 1];
    const p3 = pts[i + 2] ?? p2;
    const c1x = p1.x + (p2.x - p0.x) / 6;
    const c1y = p1.y + (p2.y - p0.y) / 6;
    const c2x = p2.x - (p3.x - p1.x) / 6;
    const c2y = p2.y - (p3.y - p1.y) / 6;
    d += ` C ${c1x.toFixed(2)} ${c1y.toFixed(2)} ${c2x.toFixed(2)} ${c2y.toFixed(2)} ${p2.x.toFixed(2)} ${p2.y.toFixed(2)}`;
  }
  return d;
}

function cut(label: string, n: number): string {
  return label.length > n ? label.slice(0, n) + '…' : label;
}

export default function MetroLine({ steps, totalPrereqs, donePrereqs, todoCount }: Props) {
  const wrapRef = useRef<HTMLDivElement | null>(null);
  // SSR 기본은 데스크톱 폭 — hydration 후 1회 측정(matchMedia render 분기 금지).
  const [width, setWidth] = useState(720);

  useEffect(() => {
    const el = wrapRef.current;
    if (!el) return;
    const measure = () => setWidth(Math.max(280, el.clientWidth));
    measure();
    if (typeof ResizeObserver === 'undefined') return;
    const ro = new ResizeObserver(measure);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  const narrow = width < 560;
  const SPINE_X = narrow ? 26 : 60;
  const R = narrow ? 10 : 13;
  const GAP = 96;
  const PAD_TOP = 66;
  const PAD_BOTTOM = 52;
  const labelX = SPINE_X + R + 14;
  const nameSize = narrow ? 17 : 19;
  const metaSize = narrow ? 10.5 : 11.5;

  const n = steps.length;
  const yOf = (i: number) => PAD_TOP + i * GAP;
  const H = PAD_TOP + (n - 1) * GAP + PAD_BOTTOM;
  const startY = PAD_TOP - 30; // 노선 시작점(다음 한 구간의 머리)

  // 스파인 샘플점: 시작점 → 각 노드(고정) + 노드 사이 중간 2점(wobble).
  const pts: { x: number; y: number }[] = [{ x: SPINE_X, y: startY }];
  let k = 0;
  for (let i = 0; i < n; i++) {
    if (i > 0) {
      const y0 = yOf(i - 1);
      const y1 = yOf(i);
      for (let t = 1; t <= 2; t++) {
        const yy = y0 + ((y1 - y0) * t) / 3;
        pts.push({ x: SPINE_X + wobble(k++, 3), y: yy });
      }
    }
    pts.push({ x: SPINE_X, y: yOf(i) });
  }
  const spineD = smoothPath(pts);
  // 다음 한 구간(시작 → 첫 역): pen-red 행진 점선 강조.
  const nextLegD = smoothPath([{ x: SPINE_X, y: startY }, { x: SPINE_X + wobble(99, 2), y: (startY + yOf(0)) / 2 }, { x: SPINE_X, y: yOf(0) - R }]);

  const go = (id: string) => { window.location.href = `/concepts/${id}`; };
  const pct = totalPrereqs > 0 ? Math.round((donePrereqs / totalPrereqs) * 100) : 0;

  return (
    <div ref={wrapRef} className="metro-wrap">
      {/* 진행 게이지 + 출발 캡션 (모눈 위, 카드 없이) */}
      <div className="metro-head">
        <div className="atlas-gauge"><i style={{ width: `${Math.max(3, pct)}%` }} /></div>
        <p className="metro-cap font-hand">
          {donePrereqs > 0
            ? `✓ ${donePrereqs}개 이수하고 출발 · ${todoCount}개 남음`
            : `${todoCount}개 학습하면 목표 도착`}
        </p>
      </div>

      <svg
        className="metro-svg"
        width={width}
        height={H}
        viewBox={`0 0 ${width} ${H}`}
        role="list"
        aria-label="학습 경로 노선"
      >
        {/* 이수 출발 구간 — hl-green 형광펜 짧은 띠 */}
        {donePrereqs > 0 && (
          <line className="metro-done" x1={SPINE_X} y1={startY - 10} x2={SPINE_X} y2={startY + 6} />
        )}

        {/* 본선 — 흑연 베이스 2겹 + 자가작도 잉크선 */}
        <path className="metro-spine-base" d={spineD} pathLength={1} />
        <path className="metro-spine" d={spineD} pathLength={1} />

        {/* 다음 한 구간 강조 (시작 → 첫 역) */}
        <path className="metro-next-leg" d={nextLegD} pathLength={1} />

        {/* 도메인 전환 띠 */}
        {steps.map((s, i) => {
          if (i === 0) return null;
          const prev = steps[i - 1];
          if (!s.domain || !prev.domain || s.domain === prev.domain) return null;
          const y = yOf(i) - GAP / 2;
          return (
            <g key={`dom-${i}`} aria-hidden="true">
              <line className="metro-domain-band" x1={SPINE_X - 9} y1={y} x2={SPINE_X + 9} y2={y} />
              <text className="metro-domain-label font-hand" x={SPINE_X + 14} y={y + 4}>
                {prev.domain}→{s.domain}
              </text>
            </g>
          );
        })}

        {/* 역(노드) */}
        {steps.map((s, i) => {
          const y = yOf(i);
          const isFrontier = i === 0 && !s.isGoal;
          return (
            <g
              key={s.id}
              className="metro-node"
              style={{ transformOrigin: `${SPINE_X}px ${y}px`, animationDelay: `${0.15 + i * 0.06}s` }}
              role="listitem"
              tabIndex={0}
              aria-label={`${s.label} · ${s.grade ?? ''} ${s.domain ?? ''} · ${s.isGoal ? '목표' : MASTERY_KO[s.mastery]}`}
              onClick={() => go(s.id)}
              onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(s.id); } }}
            >
              <title>{s.label}</title>

              {/* frontier 펄스 후광 (scale 기반 — r 애니 금지) */}
              {isFrontier && (
                <circle className="metro-frontier-halo" cx={SPINE_X} cy={y} r={R + 6} fill="none" stroke="var(--pen-green)" strokeWidth={2.4} />
              )}
              {/* 목표 금테 외륜 */}
              {s.isGoal && (
                <circle cx={SPINE_X} cy={y} r={R * 1.5 + 5} fill="none" stroke="var(--atlas-gold)" strokeWidth={2.2} />
              )}

              {/* 본체 */}
              <circle cx={SPINE_X} cy={y} r={s.isGoal ? R * 1.5 : R} {...bodyProps(s.mastery, s.isGoal)} />
              {/* 숙달 내부 가는 링 */}
              {!s.isGoal && s.mastery === 'mastered' && (
                <circle cx={SPINE_X} cy={y} r={R - 5} fill="none" stroke="var(--paper-page)" strokeWidth={1.4} />
              )}

              {/* 목표 깃발 + 도장 클라이맥스 */}
              {s.isGoal && (
                <>
                  <path className="metro-flag" d={`M ${SPINE_X + R * 1.5 + 2} ${y - 4} l 0 -20 l 15 5 l -15 5`} />
                  <circle className="metro-stamp" cx={SPINE_X} cy={y} r={R * 1.5 + 11} fill="none" pathLength={1} />
                </>
              )}

              {/* 라벨: 개념명(손글씨) + 메타 + mastery */}
              <text className="metro-name font-hand" x={labelX} y={y - 5} style={{ fontSize: nameSize }}>
                {cut(s.label, narrow ? 12 : 20)}{s.isGoal ? ' · 목표' : ''}
              </text>
              <text className="metro-meta" x={labelX} y={y + 13} style={{ fontSize: metaSize }}>
                {[s.grade, s.domain].filter(Boolean).join(' · ')}
                {!s.isGoal && (
                  <tspan dx="7" fill={MASTERY_VAR[s.mastery]}>[{MASTERY_KO[s.mastery]}]</tspan>
                )}
                {isFrontier && <tspan dx="7" className="metro-here" fill="var(--pen-green)">◜여기부터</tspan>}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}
