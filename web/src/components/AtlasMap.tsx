import { useCallback, useRef, useState } from 'react';
import type { Atlas, AtlasUnit, AtlasRouteLeg } from '../lib/atlas';
import { TYPE_LABEL_KO } from '../lib/concept-meta';

/* ════════════════════════════════════════════════════════════════════
   AtlasMap — 「항해 지도」 단원 아일랜드 (시안 B-v2 / public/mockups/map.html)
   ─────────────────────────────────────────────────────────────────────
   props.atlas(= buildAtlas 산출물)만 신뢰해 SVG 지도를 렌더한다.
   • 도메인 워시+해안선(잉크 인트로) · 길/다리 에지 · 심도 4단계 노드
   • frontier 펄스 · locked 자물쇠 · here ✕ · due 깃발 · 오늘의 항로(ants)
   • 팬(드래그)/줌(휠) — viewBox 조작, 클램프
   • 단원 클릭 → 지도 컬럼 내부 우측 슬라이드 시트(계기판을 덮지 않음)
   색은 전부 CSS 토큰(var) — html.dark 자동 추종. 애니메이션은 CSS만(JS 루프 0).
   ════════════════════════════════════════════════════════════════════ */

// 심도(depth) → 한글 태그. 인덱스 = AtlasUnit.depth.
const DEPTH_TAG = ['미답 — 윤곽만', '답사 — 연필 해칭', '정착 — 코어 잉크', '개척 완료 — 금테'] as const;

// 한글 세그먼트 안전 인코딩: '/' 경계는 보존하고 각 세그먼트만 인코딩한다.
// (슬러그가 "algebra/high-1/다항식" 형태라 통째 encodeURI 하면 한글이 깨지거나
//  반대로 encodeURIComponent 하면 '/'까지 %2F 로 먹어버린다.)
function encodeSlugPath(slug: string): string {
  return slug.split('/').map(encodeURIComponent).join('/');
}

// 단원 입장 href: 첫 미완 멤버 개념 페이지. enterSlug 없으면 null.
function enterHref(u: AtlasUnit): string | null {
  return u.enterSlug ? `/concepts/${encodeSlugPath(u.enterSlug)}` : null;
}

// ── 줌 클램프 경계(viewBox 폭) ─────────────────────────────
const VB_MIN = 520;   // 최대 확대
const VB_MAX = 2600;  // 최대 축소

export default function AtlasMap({ atlas }: { atlas: Atlas }) {
  const { width, height } = atlas;

  // viewBox(팬/줌) — 초기엔 캔버스 전체. 종횡비는 width/height 고정.
  const [vb, setVb] = useState({ x: 0, y: 0, w: width, h: height });
  const [selected, setSelected] = useState<AtlasUnit | null>(null);

  const wrapRef = useRef<HTMLDivElement | null>(null);
  // 드래그 상태(리렌더 유발 안 하도록 ref) — 시작 좌표 + 시작 viewBox 원점.
  const dragRef = useRef<{ px: number; py: number; vx: number; vy: number } | null>(null);
  const [dragging, setDragging] = useState(false);

  // ── 팬: 포인터 드래그(노드 클릭은 제외) ──────────────────
  const onPointerDown = useCallback((e: React.PointerEvent) => {
    // 노드/시트/버튼 위에서 시작한 드래그는 무시(클릭 우선).
    if ((e.target as Element).closest('[data-unit],[data-no-pan]')) return;
    dragRef.current = { px: e.clientX, py: e.clientY, vx: vb.x, vy: vb.y };
    setDragging(true);
    (e.currentTarget as Element).setPointerCapture(e.pointerId);
  }, [vb.x, vb.y]);

  const onPointerMove = useCallback((e: React.PointerEvent) => {
    const d = dragRef.current;
    if (!d) return;
    const el = wrapRef.current;
    if (!el) return;
    // 화면 픽셀 → viewBox 단위 환산(현재 줌 비율).
    const k = vb.w / el.clientWidth;
    setVb((s) => ({ ...s, x: d.vx - (e.clientX - d.px) * k, y: d.vy - (e.clientY - d.py) * k }));
  }, [vb.w]);

  const endPan = useCallback(() => {
    dragRef.current = null;
    setDragging(false);
  }, []);

  // ── 줌: 휠(커서 기준 확대/축소, 클램프) ───────────────────
  const onWheel = useCallback((e: React.WheelEvent) => {
    e.preventDefault();
    const el = wrapRef.current;
    if (!el) return;
    const factor = e.deltaY > 0 ? 1.12 : 0.89;
    const nw = Math.min(VB_MAX, Math.max(VB_MIN, vb.w * factor));
    const r = nw / vb.w;                 // 실제 적용 비율(클램프 반영)
    const rect = el.getBoundingClientRect();
    const ox = e.clientX - rect.left;
    const oy = e.clientY - rect.top;
    // 커서 아래 지점을 고정점으로 유지.
    const mx = vb.x + (ox / el.clientWidth) * vb.w;
    const my = vb.y + (oy / el.clientHeight) * vb.h;
    setVb({ x: mx - (mx - vb.x) * r, y: my - (my - vb.y) * r, w: nw, h: vb.h * r });
  }, [vb]);

  const enter = selected ? enterHref(selected) : null;

  return (
    <div className="atlas-stage" ref={wrapRef}>
      <svg
        className={`atlas-svg${dragging ? ' is-dragging' : ''}`}
        viewBox={`${vb.x} ${vb.y} ${vb.w} ${vb.h}`}
        xmlns="http://www.w3.org/2000/svg"
        role="img"
        aria-label="단원 항해 지도"
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={endPan}
        onPointerCancel={endPan}
        onWheel={onWheel}
      >
        <AtlasDefs />
        <Washes domains={atlas.domains} />
        <Coasts domains={atlas.domains} />
        <DomainLabels domains={atlas.domains} />
        <Roads edges={atlas.edges} />
        <Units units={atlas.units} onPick={setSelected} />
        <Route route={atlas.route} units={atlas.units} />
      </svg>

      <UnitSheet
        unit={selected}
        enterHref={enter}
        onClose={() => setSelected(null)}
      />
    </div>
  );
}

/* ── SVG defs: depth-1(답사) 노드의 연필 해칭 패턴 ───────────────────── */
function AtlasDefs() {
  return (
    <defs>
      <pattern
        id="atlas-hatch"
        width="6.5"
        height="6.5"
        patternUnits="userSpaceOnUse"
        patternTransform="rotate(45)"
      >
        {/* 해칭선 색은 토큰 var — 다크에서도 초크 계열로 자동 전환 */}
        <line x1="0" y1="0" x2="0" y2="6.5" stroke="var(--atlas-hatch-ink)" strokeWidth="1.5" />
      </pattern>
    </defs>
  );
}

/* ── 도메인 워시(대륙 저알파 채움) — 잉크 인트로 1단계 ─────────────────
   d.color 는 고정 hex 가 아니라 CSS 토큰 참조('var(--pen-green)' 류, atlas.ts) →
   fill/stroke 에 그대로 넣어도 html.dark 에서 초크 톤으로 자동 추종(워시·해안선·지명 공통). */
function Washes({ domains }: { domains: Atlas['domains'] }) {
  return (
    <g aria-hidden="true">
      {domains.map((d, i) => (
        <path
          key={d.key}
          className="atlas-wash"
          style={{ animationDelay: `${0.05 + i * 0.1}s` }}
          d={d.path}
          fill={d.color}
          fillOpacity={0.08}
        />
      ))}
    </g>
  );
}

/* ── 해안선(대륙 윤곽) — 잉크 인트로 2단계(stroke draw) ──────────────── */
function Coasts({ domains }: { domains: Atlas['domains'] }) {
  return (
    <g aria-hidden="true">
      {domains.map((d, i) => (
        <path
          key={d.key}
          className="atlas-coast"
          style={{ animationDelay: `${0.2 + i * 0.1}s` }}
          d={d.path}
          stroke={d.color}
        />
      ))}
    </g>
  );
}

/* ── 도메인 지명(라벨 · 개수) — 잉크 인트로 3단계 ───────────────────── */
function DomainLabels({ domains }: { domains: Atlas['domains'] }) {
  return (
    <g aria-hidden="true">
      {domains.map((d, i) => (
        <text
          key={d.key}
          className="atlas-dlabel"
          style={{ animationDelay: `${0.9 + i * 0.1}s` }}
          x={d.cx}
          y={d.cy}
          fill={d.color}
          textAnchor="middle"
        >
          {d.label} · {d.count}
        </text>
      ))}
    </g>
  );
}

/* ── 길(선수 에지) — bridge(크로스도메인)는 점선 다리 ────────────────
   직선 세그먼트를 살짝 곡선화(연필로 그은 길의 손맛). 곡률 부호·크기는
   좌표 합 기반 결정적 — SSR 매 요청 동일(난수 금지). ─────────────────── */
function roadPath(e: Atlas['edges'][number]): string {
  const mx = (e.x1 + e.x2) / 2;
  const my = (e.y1 + e.y2) / 2;
  const dx = e.x2 - e.x1;
  const dy = e.y2 - e.y1;
  const len = Math.hypot(dx, dy) || 1;
  // 세그먼트에 수직인 단위벡터 × 결정적 부호(좌표합 짝/홀) × 약한 진폭.
  const sign = (Math.round(e.x1 + e.y1) % 2 === 0) ? 1 : -1;
  const amp = Math.min(18, len * 0.08) * sign;
  const cx = mx + (-dy / len) * amp;
  const cy = my + (dx / len) * amp;
  return `M${e.x1.toFixed(1)},${e.y1.toFixed(1)} Q${cx.toFixed(1)},${cy.toFixed(1)} ${e.x2.toFixed(1)},${e.y2.toFixed(1)}`;
}

function Roads({ edges }: { edges: Atlas['edges'] }) {
  return (
    <g className="atlas-roads" aria-hidden="true">
      {edges.map((e, i) => (
        <path
          key={i}
          className={`atlas-road${e.bridge ? ' is-bridge' : ''}`}
          style={{ animationDelay: `${1.1 + i * 0.02}s` }}
          d={roadPath(e)}
        />
      ))}
    </g>
  );
}

/* ── 단원 노드(심도 4단계 + 상태 배지) ──────────────────────────────── */
const R = 11; // 노드 본체 반지름

// depth → 본체 circle 의 fill/stroke 프레젠테이션 속성.
function bodyProps(u: AtlasUnit): React.SVGProps<SVGCircleElement> {
  switch (u.depth) {
    case 1: // 답사 — 연필 해칭
      return { fill: 'url(#atlas-hatch)', stroke: 'var(--ink-soft)', strokeWidth: 1.8 };
    case 2: // 정착 — 코어 잉크
      return { fill: 'var(--color-accent)', stroke: 'var(--color-accent-strong)', strokeWidth: 1.8 };
    case 3: // 개척 완료 — 금테 이중링
      return { fill: 'var(--color-accent)', stroke: 'var(--atlas-gold)', strokeWidth: 3 };
    default: // 0 미답 — 윤곽만(잠김이면 솔리드 채움)
      return {
        fill: u.locked ? 'var(--paper-well)' : 'var(--paper-page)',
        stroke: 'var(--paper-dim)',
        strokeWidth: 1.8,
        strokeDasharray: u.locked ? undefined : '3 3',
      };
  }
}

// 라벨 밀도: 미답·잠김은 작게/흐리게, frontier·진행중·깃발은 또렷하게.
function labelClass(u: AtlasUnit): string {
  if (u.frontier || u.here || u.dueCount > 0 || u.depth >= 2) return 'atlas-ulabel is-strong';
  if (u.locked || u.depth === 0) return 'atlas-ulabel is-faint';
  return 'atlas-ulabel';
}

function UnitNode({ u, onPick, i }: { u: AtlasUnit; onPick: (u: AtlasUnit) => void; i: number }) {
  const flags = Math.min(2, Math.max(0, u.dueCount)); // due 깃발은 최대 2개
  return (
    <g
      data-unit={u.id}
      className={`atlas-unit${u.locked ? ' is-locked' : ''}`}
      style={{ animationDelay: `${1.15 + i * 0.045}s`, transformOrigin: `${u.x}px ${u.y}px` }}
      role="button"
      tabIndex={0}
      aria-label={`${u.label} · ${DEPTH_TAG[u.depth]} · ${u.pct}%`}
      onClick={() => onPick(u)}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onPick(u);
        }
      }}
    >
      {/* frontier 초록 펄스 후광 */}
      {u.frontier && (
        <circle className="atlas-frontier-halo" cx={u.x} cy={u.y} r={17} fill="none" stroke="var(--pen-green)" strokeWidth={2.4} />
      )}

      {/* 본체 */}
      <circle className="atlas-body" cx={u.x} cy={u.y} r={R} {...bodyProps(u)} />
      {/* 개척(depth 3) 내부 금테 이중링 */}
      {u.depth === 3 && (
        <circle cx={u.x} cy={u.y} r={6.2} fill="none" stroke="var(--paper-page)" strokeWidth={1.4} />
      )}

      {/* 잠김 자물쇠 */}
      {u.locked && (
        <text className="atlas-glyph" x={u.x} y={u.y + 4} fontSize={10} textAnchor="middle">🔒</text>
      )}
      {/* 현재 위치 ✕ */}
      {u.here && (
        <text className="atlas-here" x={u.x - 7} y={u.y - 15} fontSize={20} textAnchor="middle">✕</text>
      )}

      {/* due 깃발(최대 2) */}
      {Array.from({ length: flags }).map((_, fi) => {
        const fx = u.x + 14 + fi * 10;
        const fy = u.y - 14;
        return (
          <g key={fi}>
            <line className="atlas-flagpole" x1={fx} y1={fy} x2={fx} y2={fy - 16} />
            <path d={`M${fx},${fy - 16} l 15,4.5 l -15,5 Z`} fill="var(--pen-red)" />
          </g>
        );
      })}

      {/* 라벨 + frontier 부제 */}
      <text className={labelClass(u)} x={u.x} y={u.y + 27} textAnchor="middle">{u.label}</text>
      {u.frontier && (
        <text className="atlas-sublabel" x={u.x} y={u.y + 40} textAnchor="middle" fill="var(--pen-green)">다음 개척지</text>
      )}
    </g>
  );
}

function Units({ units, onPick }: { units: AtlasUnit[]; onPick: (u: AtlasUnit) => void }) {
  return (
    <g className="atlas-units">
      {units.map((u, i) => (
        <UnitNode key={u.id} u={u} i={i} onPick={onPick} />
      ))}
    </g>
  );
}

/* ── 오늘의 항로(0~3 구간) ──────────────────────────────────────────────
   UX 결함 해결:
   (3) 점선이 노드를 정통으로 지나 라벨을 가림 → 경유 노드를 비껴가는 베지어.
   (1) waypoint 라벨이 단원 라벨과 겹침 → 노드에서 충분히 오프셋 + stroke 후광
       + 가까운 단원과 충돌 시 반대편 배치.
   ─────────────────────────────────────────────────────────────────────── */

// 노드 본체/라벨이 점유하는 대략 반경(이 안을 항로가 가로지르지 않도록).
const NODE_AVOID = 30;

type Pt = { x: number; y: number };

// 구간 A→B 사이를 잇는 베지어. 중간 근처 단원 노드가 있으면 그 반대로 휜다.
function legPath(a: Pt, b: Pt, units: AtlasUnit[]): string {
  const mx = (a.x + b.x) / 2;
  const my = (a.y + b.y) / 2;
  const dx = b.x - a.x;
  const dy = b.y - a.y;
  const len = Math.hypot(dx, dy) || 1;
  const nx = -dy / len; // 수직 단위벡터
  const ny = dx / len;

  // 중점에서 가장 가까운(끝점 제외) 단원을 찾아 그 반대 방향으로 우회.
  let bow = Math.min(36, len * 0.12); // 기본 완만한 곡률
  let best: AtlasUnit | null = null;
  let bestD = Infinity;
  for (const u of units) {
    const d = Math.hypot(u.x - mx, u.y - my);
    if (d < bestD && d < 90) { bestD = d; best = u; }
  }
  let sign = 1;
  if (best) {
    // 단원이 수직선의 어느 쪽인지 → 그 반대쪽으로 휘게 부호 결정.
    const side = (best.x - mx) * nx + (best.y - my) * ny;
    sign = side > 0 ? -1 : 1;
    bow = Math.max(bow, NODE_AVOID + 14 - Math.min(bestD, NODE_AVOID)); // 가까울수록 더 크게
  }
  const off = bow * sign;
  // 제어점 둘 다 같은 쪽으로 밀어 부드러운 호.
  const c1x = a.x + dx * 0.33 + nx * off;
  const c1y = a.y + dy * 0.33 + ny * off;
  const c2x = a.x + dx * 0.66 + nx * off;
  const c2y = a.y + dy * 0.66 + ny * off;
  return `C${c1x.toFixed(1)},${c1y.toFixed(1)} ${c2x.toFixed(1)},${c2y.toFixed(1)} ${b.x.toFixed(1)},${b.y.toFixed(1)}`;
}

// 항로 전체 패스(각 구간 베지어 이어붙임).
function routeD(legs: AtlasRouteLeg[], units: AtlasUnit[]): string {
  if (legs.length === 0) return '';
  let d = `M${legs[0].x.toFixed(1)},${legs[0].y.toFixed(1)}`;
  for (let i = 1; i < legs.length; i++) {
    d += ' ' + legPath(legs[i - 1], legs[i], units);
  }
  return d;
}

// 항로 구간 종류별 글리프.
const LEG_GLYPH: Record<AtlasRouteLeg['kind'], string> = {
  review: '⚑',
  continue: '✕',
  problem: '★',
};

// waypoint 라벨 위치: 노드에서 오프셋 + 가까운 단원과 충돌하면 반대편으로.
// 반환 {lx, ly, anchor}. 결정적(난수 없음).
function labelSpot(leg: AtlasRouteLeg, units: AtlasUnit[]): { lx: number; ly: number; anchor: 'start' | 'end' | 'middle' } {
  const OFF_X = 18;
  const OFF_Y = 24; // 노드 자체 라벨(y+27)과 겹치지 않게 위로 띄움
  // 후보: 좌상 / 우상 / 정상단.
  const candidates: { lx: number; ly: number; anchor: 'start' | 'end' | 'middle' }[] = [
    { lx: leg.x - OFF_X, ly: leg.y - OFF_Y, anchor: 'end' },
    { lx: leg.x + OFF_X, ly: leg.y - OFF_Y, anchor: 'start' },
    { lx: leg.x, ly: leg.y - OFF_Y - 14, anchor: 'middle' },
  ];
  // 라벨 앵커점이 단원 노드 중심과 충분히 떨어진 첫 후보 선택.
  for (const c of candidates) {
    let clear = true;
    for (const u of units) {
      if (u.id === leg.unitId) continue; // 자기 단원 노드는 라벨 주인이라 무시
      if (Math.hypot(u.x - c.lx, u.y - c.ly) < 34) { clear = false; break; }
    }
    if (clear) return c;
  }
  return candidates[0]; // 전부 충돌 시 좌상 기본
}

function Route({ route, units }: { route: AtlasRouteLeg[]; units: AtlasUnit[] }) {
  if (route.length === 0) return null;
  const d = routeD(route, units);
  return (
    <g aria-hidden="true">
      {d && <path className="atlas-route" d={d} />}
      {route.map((leg, i) => {
        const s = labelSpot(leg, units);
        return (
          <text
            key={i}
            className="atlas-waypt"
            style={{ animationDelay: `${2.1 + i * 0.12}s` }}
            x={s.lx}
            y={s.ly}
            textAnchor={s.anchor}
          >
            {LEG_GLYPH[leg.kind]} {leg.label}
          </text>
        );
      })}
    </g>
  );
}

/* ── 단원 시트(지도 컬럼 내부 우측 슬라이드) ─────────────────────────── */

// 개념 타입 키 → 색 토큰. concept-graph 의 concept_type 값(정의/정리/예제 …)을
// TYPE_LABEL_KO 라벨로도, 영문 키로도 받을 수 있게 양쪽 매핑.
const TYPE_DOT: Record<string, string> = {
  definition: 'var(--color-accent)', 정의: 'var(--color-accent)',
  theorem: 'var(--pen-violet)', 정리: 'var(--pen-violet)',
  lemma: 'var(--pen-cyan)', 보조정리: 'var(--pen-cyan)',
  example: 'var(--pen-green)', 예제: 'var(--pen-green)',
};
function typeDot(key: string, label: string): string {
  return TYPE_DOT[key] ?? TYPE_DOT[label] ?? 'var(--ink-soft)';
}
// 한글 라벨 보장: 영문 키면 TYPE_LABEL_KO 로 변환, 이미 한글이면 그대로.
function typeLabelKo(key: string, fallback: string): string {
  return TYPE_LABEL_KO[key] ?? fallback;
}

function UnitSheet({
  unit,
  enterHref,
  onClose,
}: {
  unit: AtlasUnit | null;
  enterHref: string | null;
  onClose: () => void;
}) {
  const open = unit !== null;
  // 시트는 항상 마운트(슬라이드 전환). 내용은 unit 있을 때만 채움.
  return (
    <aside
      className={`atlas-sheet${open ? ' is-open' : ''}`}
      data-no-pan
      role="dialog"
      aria-modal="false"
      aria-hidden={!open}
      aria-label={unit ? `${unit.label} 단원 상세` : undefined}
    >
      {unit && <SheetBody unit={unit} enterHref={enterHref} onClose={onClose} />}
    </aside>
  );
}

function SheetBody({
  unit: u,
  enterHref,
  onClose,
}: {
  unit: AtlasUnit;
  enterHref: string | null;
  onClose: () => void;
}) {
  const graphHref = `/graph?highlight=${encodeURIComponent(u.id)}`;
  // unit 타입 제외한 분류만(계약상 types 에 이미 unit 제외됨).
  const types = u.types;
  return (
    <>
      <button className="atlas-sheet-close" data-no-pan onClick={onClose} aria-label="닫기">닫기 ✕</button>

      <div className="atlas-crumb">{u.id}</div>
      <h2 className="atlas-sheet-title">{u.label}</h2>

      <div className="atlas-meta">
        {u.grade && <span className="atlas-chip">{u.grade}</span>}
        {u.domain && <span className="atlas-chip">{u.domain}</span>}
        <span className="atlas-chip">{u.spokeCount}개 개념</span>
      </div>

      <span className={`atlas-depth-tag d${u.depth}`}>{DEPTH_TAG[u.depth]}</span>
      <div className="atlas-gauge"><i style={{ width: `${u.pct}%` }} /></div>
      <div className="atlas-pct">심도 {u.pct}%</div>

      {u.locked && u.lockedBy.length > 0 && (
        <div className="atlas-lockbox">
          🔒 잠김 — 선수 단원 <b>{u.lockedBy.join(' · ')}</b> 가 정착(proficient+) 되면 자동 해제됩니다.
        </div>
      )}

      {u.dueCount > 0 && (
        <div className="atlas-due">⚑ 복습 대기 {u.dueCount}건 — 깃발부터 걷어내면 좋아요.</div>
      )}

      {types.length > 0 && (
        <div className="atlas-tsec">
          <h4>이 단원의 개념 — 타입별 (보조)</h4>
          {types.map((t) => (
            <div className="atlas-trow" key={t.key}>
              <span className="atlas-tdot" style={{ background: typeDot(t.key, t.label) }} />
              {typeLabelKo(t.key, t.label)}
              <span className="atlas-tcnt">{t.done}/{t.total}</span>
            </div>
          ))}
        </div>
      )}

      {/* 입장 — enterSlug 있을 때만 실링크. 잠김/슬러그 없으면 비활성 표시. */}
      {enterHref && !u.locked ? (
        <a className="atlas-enter" href={enterHref}>
          ⛺ 입장 — {u.depth === 0 ? '첫 발 딛기' : '이어서 배우기'}
        </a>
      ) : (
        <span className="atlas-enter is-disabled" aria-disabled="true">
          ⛺ 입장 — {u.locked ? '잠김' : '준비 중'}
        </span>
      )}

      <a className="atlas-graph-link" href={graphHref}>◈ 상세 그래프 → /graph</a>
    </>
  );
}
