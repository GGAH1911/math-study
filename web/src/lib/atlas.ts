// ════════════════════════════════════════════════════════════════════════
// Atlas — /index 항해 지도의 단일 데이터 빌더.
//
// concept-graph.json 의 단원 토폴로지 + health.ts 의 락/언락 골드 스탠다드를
// 결정적(SSR-안전) 좌표 레이아웃으로 투영한다. 난수 금지 — 같은 입력이면 매 요청
// 동일한 지도가 나와야 한다(서버 렌더 흔들림 방지).
//
// 락·언락 로직(recommendUnits().ready = 선수 단원 전부 proficient+)은 재구현하지
// 않고 그대로 소비한다. 여기서 새로 계산하는 것은 "어디에 그릴지"(좌표·블롭·항로)뿐.
// ════════════════════════════════════════════════════════════════════════
import {
  readConceptGraph,
  computeUnitProgress,
  recommendUnits,
  GRADE_RANK,
  type UnitStatus,
  type UnitProgress,
  type ConceptGraph,
} from './health.ts';
import { TYPE_LABEL_KO } from './concept-meta.ts';

// ── 외부 계약 타입 (I2/I3 는 이 모양만 신뢰) ──────────────────────────────
export type AtlasUnitType = { key: string; label: string; total: number; done: number };

export type AtlasUnit = {
  id: string; label: string; grade?: string; domain?: string;
  x: number; y: number;
  depth: 0 | 1 | 2 | 3;       // status: unknown0 learning1 proficient2 mastered3 (미답/답사/정착/개척)
  pct: number;                // progressPercent
  locked: boolean;            // pct===0 && !frontier
  frontier: boolean;          // recommendUnits().ready 멤버 (락·언락 그대로)
  here: boolean;              // continuing[0] (없으면 전부 false)
  dueCount: number;           // 이 단원 멤버 중 사용자 due 개념 수
  lockedBy: string[];         // 미충족 선수 단원 label 목록 (locked 일 때)
  types: AtlasUnitType[];     // TYPE_LABEL_KO 기반 단원 내 타입별 {total, done(proficient+)} — unit 타입 제외
  enterSlug: string | null;   // 첫 미완 멤버 개념 slug (전부 완이면 첫 멤버, 멤버 0이면 null)
  spokeCount: number;
};

export type AtlasDomain = {
  key: string; label: string; count: number;
  cx: number; cy: number; path: string;
  color: string;  // CSS 토큰 참조(예: 'var(--pen-green)') — 고정 hex 아님(다크 자동 추종)
};

export type AtlasEdge = { x1: number; y1: number; x2: number; y2: number; bridge: boolean };

export type AtlasRouteLeg = {
  kind: 'review' | 'continue' | 'problem';
  unitId?: string; label: string; x: number; y: number; href: string;
};

export type Atlas = {
  width: number; height: number;
  domains: AtlasDomain[];
  units: AtlasUnit[];
  edges: AtlasEdge[];
  route: AtlasRouteLeg[];
  depthCounts: [number, number, number, number];
};

// ── 레이아웃 상수 ────────────────────────────────────────────────────────
const WIDTH = 1500;
const HEIGHT = 950;

// 도메인 앵커(고정). 미지정 도메인은 폴백 앵커로 모인다.
const DOMAIN_ANCHOR: Record<string, { x: number; y: number }> = {
  '수와식':   { x: 300,  y: 250 },
  '방정식':   { x: 720,  y: 190 },
  '논리':     { x: 1080, y: 150 },
  '함수':     { x: 840,  y: 580 },
  '도형':     { x: 300,  y: 660 },
  '확률통계': { x: 1230, y: 640 },
};
const FALLBACK_ANCHOR = { x: 1080, y: 400 };

// 도메인별 워시/해안선/지명 색 — 고정 hex 금지(라이트 hex가 다크에서도 그대로 칠해져
// 대비 저하). CSS 토큰 참조 문자열만 산출하고, var(--pen-*) 는 html.dark 에서 초크 톤으로
// 자동 밝아진다(global.css). AtlasMap 은 이 값을 그대로 fill/stroke 에 주입.
const DOMAIN_TOKEN: Record<string, string> = {
  '수와식':   'var(--pen-cyan)',
  '방정식':   'var(--pen-red)',
  '함수':     'var(--pen-green)',
  '도형':     'var(--pen-amber)',
  '확률통계': 'var(--pen-violet)',
  '논리':     'var(--color-accent)',
};
const FALLBACK_TOKEN = 'var(--ink-muted)';

// status → depth. 동일 순서(미답0 답사1 정착2 개척3).
const STATUS_DEPTH: Record<UnitStatus, 0 | 1 | 2 | 3> = {
  unknown: 0, learning: 1, proficient: 2, mastered: 3,
};

type GNode = ConceptGraph['nodes'][number];

// ── 결정적 헬퍼 ────────────────────────────────────────────────────────────
// 모든 흔들림(wobble)은 sin 기반 결정적 노이즈 — Math.random 절대 금지.
const TAU = Math.PI * 2;
const GOLDEN_ANGLE = 2.39996; // 라디안. phyllotaxis(해바라기 씨) 배치각.

// seed·인덱스로 [-1,1] 범위의 결정적 흔들림.
function wobble(i: number, k: number, seed: number): number {
  return Math.sin(i * k + seed);
}

// 도메인 내 단원 좌표: GRADE_RANK→label 정렬은 호출부에서 끝내고, 정렬된 i 로 골든앵글 배치.
// r = spacing*√i 라 중심에서 바깥으로 고르게 퍼진다. 단원 1~3개 도메인은 spacing 을 키워 안 겹치게.
function phyllotaxis(i: number, spacing: number): { dx: number; dy: number } {
  const theta = i * GOLDEN_ANGLE;
  const r = spacing * Math.sqrt(i);
  return { dx: Math.cos(theta) * r, dy: Math.sin(theta) * r };
}

// 점군을 감싸는 wobbly 닫힌 SVG 패스. 중심·반경에서 각도별로 r 을 살짝 흔들어 손그림 해안선 느낌.
// (extent + 패딩으로 반경 산출 → 16분할 베지어 루프.) 점이 1개여도 최소 반경 보장.
function blobPath(
  pts: { x: number; y: number }[],
  padding: number,
  seed: number,
): { path: string; cx: number; cy: number } {
  const cx = pts.reduce((a, p) => a + p.x, 0) / pts.length;
  const cy = pts.reduce((a, p) => a + p.y, 0) / pts.length;
  // 중심에서 가장 먼 점 + 패딩 → 기본 반경. 한 점 클러스터도 최소 반경 확보.
  let maxR = 0;
  for (const p of pts) maxR = Math.max(maxR, Math.hypot(p.x - cx, p.y - cy));
  const baseR = Math.max(maxR + padding, 70);

  // 16개 둘레점을 각도별 흔들린 반경으로 잡고 Catmull-Rom→Cubic 으로 부드러운 닫힌 곡선.
  const N = 16;
  const ring: { x: number; y: number }[] = [];
  for (let a = 0; a < N; a++) {
    const ang = (a / N) * TAU;
    // 두 주파수 합으로 균일하지 않은(손맛) 둘레. 진폭은 반경의 ~12%.
    const w = wobble(a, 1, seed) * 0.5 + wobble(a, 2.3, seed + 1.7) * 0.5;
    const r = baseR * (1 + 0.12 * w);
    ring.push({ x: cx + Math.cos(ang) * r, y: cy + Math.sin(ang) * r });
  }
  return { path: catmullRomLoop(ring), cx, cy };
}

// 닫힌 점 루프를 Catmull-Rom 보간한 cubic-bezier 패스 문자열로. (둘레 흔들림을 부드럽게 잇는다.)
function catmullRomLoop(p: { x: number; y: number }[]): string {
  const n = p.length;
  const f = (v: number) => Math.round(v * 10) / 10; // 좌표 소수 1자리(패스 길이 절약 + 결정성)
  let d = `M${f(p[0].x)},${f(p[0].y)}`;
  for (let i = 0; i < n; i++) {
    const p0 = p[(i - 1 + n) % n];
    const p1 = p[i];
    const p2 = p[(i + 1) % n];
    const p3 = p[(i + 2) % n];
    const c1x = p1.x + (p2.x - p0.x) / 6;
    const c1y = p1.y + (p2.y - p0.y) / 6;
    const c2x = p2.x - (p3.x - p1.x) / 6;
    const c2y = p2.y - (p3.y - p1.y) / 6;
    d += ` C${f(c1x)},${f(c1y)} ${f(c2x)},${f(c2y)} ${f(p2.x)},${f(p2.y)}`;
  }
  return d + 'Z';
}

// 두 점을 잇되 경유점(노드) 위를 정통으로 지나지 않게 살짝 우회하는 2차 베지어.
// (스크린샷 결함 #3: 항로 점선이 노드를 관통해 라벨을 가림 → 중점을 법선방향으로 밀어 회피.)
// 항로 컴포넌트(AtlasMap)가 route leg 좌표를 이 헬퍼로 이어 그린다 — bow 양수=좌측 활.
export function curvedLeg(
  x1: number, y1: number, x2: number, y2: number, bow: number,
): string {
  const mx = (x1 + x2) / 2;
  const my = (y1 + y2) / 2;
  const dx = x2 - x1;
  const dy = y2 - y1;
  const len = Math.hypot(dx, dy) || 1;
  // 법선(좌측) 방향으로 중점을 bow 만큼 밀어 완만한 활.
  const nx = -dy / len;
  const ny = dx / len;
  const cx = mx + nx * bow;
  const cy = my + ny * bow;
  const f = (v: number) => Math.round(v * 10) / 10;
  return `M${f(x1)},${f(y1)} Q${f(cx)},${f(cy)} ${f(x2)},${f(y2)}`;
}

// ── buildAtlas ────────────────────────────────────────────────────────────
export function buildAtlas(
  masteryOf: (id: string) => UnitStatus,
  dueConceptIds: Set<string>,
): Atlas {
  const graph = readConceptGraph();
  const unitNodes = graph.nodes.filter((n) => n.concept_type === 'unit');

  // 진행도/추천은 health.ts 그대로 — 락·언락 재구현 금지.
  const progress = computeUnitProgress(masteryOf);
  const progById = new Map<string, UnitProgress>(progress.map((p) => [p.unitId, p]));
  const { continuing, ready } = recommendUnits(masteryOf);
  const frontierIds = new Set(ready.map((u) => u.unitId));
  const hereId = continuing[0]?.unitId ?? null;

  const unitNodeById = new Map<string, GNode>(unitNodes.map((n) => [n.id, n]));
  const labelById = new Map<string, string>(unitNodes.map((n) => [n.id, n.label]));

  // 멤버(스포크) 귀속: home_unit 기준. 단원별 멤버 리스트(단원 노드 자신 제외 — types/enterSlug 용).
  const membersByUnit = new Map<string, GNode[]>();
  for (const u of unitNodes) membersByUnit.set(u.id, []);
  for (const n of graph.nodes) {
    if (n.concept_type === 'unit') continue;
    const home = n.home_unit;
    if (home && membersByUnit.has(home)) membersByUnit.get(home)!.push(n);
  }

  // ── 1) 도메인별 단원 묶기 + 결정적 좌표 ──────────────────────────────────
  const byDomain = new Map<string, GNode[]>();
  for (const u of unitNodes) {
    const dom = u.domain ?? '__none__';
    (byDomain.get(dom) ?? byDomain.set(dom, []).get(dom)!).push(u);
  }

  const coord = new Map<string, { x: number; y: number }>();
  for (const [dom, members] of byDomain) {
    const anchor = DOMAIN_ANCHOR[dom] ?? FALLBACK_ANCHOR;
    // 정렬: 학년 순 → 라벨(ko). 결정적.
    const sorted = [...members].sort(
      (a, b) =>
        (GRADE_RANK[a.grade ?? ''] ?? 9) - (GRADE_RANK[b.grade ?? ''] ?? 9) ||
        a.label.localeCompare(b.label, 'ko-KR'),
    );
    const spacing = sorted.length <= 3 ? 60 : 48;
    // 도메인 시드: 앵커 좌표로 — 도메인마다 wobble 위상 다르게(결정적).
    const seed = (anchor.x * 0.013 + anchor.y * 0.017) % TAU;
    sorted.forEach((u, i) => {
      const { dx, dy } = phyllotaxis(i, spacing);
      // 배치 자체에도 미세 흔들림(격자 느낌 제거). 진폭 작게.
      const jx = wobble(i, 1.7, seed) * 6;
      const jy = wobble(i, 2.1, seed + 0.9) * 6;
      coord.set(u.id, { x: anchor.x + dx + jx, y: anchor.y + dy + jy });
    });
  }

  // ── 2) 단원 객체 빌드 ────────────────────────────────────────────────────
  const depthCounts: [number, number, number, number] = [0, 0, 0, 0];
  const units: AtlasUnit[] = unitNodes.map((node) => {
    const p = progById.get(node.id)!;
    const status = p.status;
    const depth = STATUS_DEPTH[status];
    const xy = coord.get(node.id) ?? FALLBACK_ANCHOR;
    const frontier = frontierIds.has(node.id);
    const locked = p.progressPercent === 0 && !frontier;
    const members = membersByUnit.get(node.id) ?? [];

    // 타입별 {total, done(proficient+)} — unit 타입 제외, TYPE_LABEL_KO 순.
    const TYPE_KEYS = ['definition', 'theorem', 'lemma', 'example'];
    const typeAgg = new Map<string, { total: number; done: number }>();
    for (const k of TYPE_KEYS) typeAgg.set(k, { total: 0, done: 0 });
    let dueCount = 0;
    for (const m of members) {
      const agg = typeAgg.get(m.concept_type);
      if (agg) {
        agg.total++;
        const lvl = masteryOf(m.id);
        if (lvl === 'proficient' || lvl === 'mastered') agg.done++;
      }
      if (dueConceptIds.has(m.id)) dueCount++;
    }
    const types: AtlasUnitType[] = TYPE_KEYS
      .map((k) => ({ key: k, label: TYPE_LABEL_KO[k] ?? k, ...typeAgg.get(k)! }))
      .filter((t) => t.total > 0);

    // 입장점: 첫 미완(미proficient) 멤버 → 없으면 첫 멤버 → 멤버 0이면 null.
    let enterSlug: string | null = null;
    if (members.length > 0) {
      const firstIncomplete = members.find((m) => {
        const lvl = masteryOf(m.id);
        return lvl !== 'proficient' && lvl !== 'mastered';
      });
      enterSlug = (firstIncomplete ?? members[0]).slug;
    }

    // 잠금 사유: 미충족 선수 단원 label. (recommendUnits 의 ready 판정과 동일 기준: proficient+.)
    const lockedBy: string[] = [];
    if (locked) {
      for (const pre of node.prerequisites ?? []) {
        const preProg = progById.get(pre);
        if (!preProg) continue; // 단원이 아닌 선수(개념)는 무시 — 단원간 락만.
        if (preProg.status !== 'proficient' && preProg.status !== 'mastered') {
          lockedBy.push(labelById.get(pre) ?? preProg.label);
        }
      }
    }

    depthCounts[depth]++;
    return {
      id: node.id,
      label: node.label,
      grade: node.grade,
      domain: node.domain,
      x: Math.round(xy.x * 10) / 10,
      y: Math.round(xy.y * 10) / 10,
      depth,
      pct: p.progressPercent,
      locked,
      frontier,
      here: hereId === node.id,
      dueCount,
      lockedBy,
      types,
      enterSlug,
      spokeCount: p.spokeCount,
    };
  });
  const unitById = new Map<string, AtlasUnit>(units.map((u) => [u.id, u]));

  // ── 3) 도메인 블롭(워시 해안선) ─────────────────────────────────────────
  const domains: AtlasDomain[] = [];
  for (const [dom, members] of byDomain) {
    if (dom === '__none__') continue; // 폴백 묶음은 블롭 없이 노드만.
    const pts = members.map((u) => coord.get(u.id)!).filter(Boolean);
    if (pts.length === 0) continue;
    const anchor = DOMAIN_ANCHOR[dom] ?? FALLBACK_ANCHOR;
    const seed = (anchor.x * 0.011 + anchor.y * 0.019) % TAU;
    const { path, cx, cy } = blobPath(pts, 75, seed);
    domains.push({
      key: dom, label: dom, count: members.length,
      cx: Math.round(cx * 10) / 10, cy: Math.round(cy * 10) / 10,
      path, color: DOMAIN_TOKEN[dom] ?? FALLBACK_TOKEN,
    });
  }

  // ── 4) 에지(선수 단원 길) — 75 에지. 크로스도메인 = bridge(점선). ──────────
  const edges: AtlasEdge[] = [];
  for (const node of unitNodes) {
    const to = unitById.get(node.id);
    if (!to) continue;
    for (const pre of node.prerequisites ?? []) {
      if (!unitNodeById.has(pre)) continue; // 단원→단원 에지만.
      const from = unitById.get(pre);
      if (!from) continue;
      const fromNode = unitNodeById.get(pre)!;
      const bridge = (fromNode.domain ?? '') !== (node.domain ?? '');
      edges.push({ x1: from.x, y1: from.y, x2: to.x, y2: to.y, bridge });
    }
  }

  // ── 5) 오늘의 항로 (review → continue → problem, 0~3 leg) ────────────────
  const route = buildRoute(units, unitById, dueConceptIds, membersByUnit, continuing, ready);

  return { width: WIDTH, height: HEIGHT, domains, units, edges, route, depthCounts };
}

// 항로 leg 구성. enterSlug 의 /concepts/<slug> 로(세그먼트별 encodeURI), null leg 는 생략.
function buildRoute(
  units: AtlasUnit[],
  unitById: Map<string, AtlasUnit>,
  dueConceptIds: Set<string>,
  membersByUnit: Map<string, GNode[]>,
  continuing: UnitProgress[],
  ready: UnitProgress[],
): AtlasRouteLeg[] {
  const legs: AtlasRouteLeg[] = [];

  // 단원 slug → /concepts URL (한글 세그먼트 인코딩, 슬래시는 보존).
  const conceptHref = (slug: string): string =>
    '/concepts/' + slug.split('/').map(encodeURIComponent).join('/');

  // ① review: dueCount 최대 단원(>0).
  let reviewUnit: AtlasUnit | null = null;
  for (const u of units) {
    if (u.dueCount > 0 && (!reviewUnit || u.dueCount > reviewUnit.dueCount)) reviewUnit = u;
  }
  if (reviewUnit && reviewUnit.enterSlug) {
    legs.push({
      kind: 'review', unitId: reviewUnit.id,
      label: `복습 ${reviewUnit.dueCount}건 — ${reviewUnit.label}`,
      x: reviewUnit.x, y: reviewUnit.y, href: conceptHref(reviewUnit.enterSlug),
    });
  }

  // ② continue: continuing[0] → 없으면 ready[0].
  const contId = continuing[0]?.unitId ?? ready[0]?.unitId ?? null;
  const contUnit = contId ? unitById.get(contId) ?? null : null;
  if (contUnit && contUnit.enterSlug && contUnit.id !== reviewUnit?.id) {
    legs.push({
      kind: 'continue', unitId: contUnit.id,
      label: `이어서 — ${contUnit.label}`,
      x: contUnit.x, y: contUnit.y, href: conceptHref(contUnit.enterSlug),
    });
  }

  // ③ problem: 확률통계 해안 고정점. 항상 존재.
  legs.push({
    kind: 'problem',
    label: '오늘의 문제',
    x: 1180, y: 760, href: '/problems',
  });

  return legs;
}
