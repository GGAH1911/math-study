// Helpers to load wiki health/log info directly from the docs/ filesystem.
// Uses process.cwd() since `npm run dev|build` is always invoked from web/.
import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import matter from 'gray-matter';

const WEB_ROOT = process.cwd();
const DOCS = resolve(WEB_ROOT, '..', 'docs');

export type Health = {
  pages: number;
  orphans: number;
  conflicts: number;
  dueToday: number;
  mastery: { unknown: number; learning: number; proficient: number; mastered: number };
  dagIntegrity: string;
  suggestedAction: string;
  lastUpdated: string;
};

export function readHealth(): Health {
  // 정량 필드(개념수·mastery·due·dag)는 *라이브* 소스인 concept-graph.json 에서 실측한다.
  // (그래프 빌드 스크립트 + mastery-promote API 가 노드를 갱신하므로 항상 최신.)
  // docs/index.md frontmatter 의 mastery_*/due_today/pages 는 2026-05-16 박제 스냅샷
  // (개념 490 시절)이라 더 이상 읽지 않는다 — 텍스트(suggested_action/last_updated)만 가져온다.
  const graph = readConceptGraph();
  const mastery = { unknown: 0, learning: 0, proficient: 0, mastered: 0 };
  for (const n of graph.nodes) {
    const k = n.mastery as keyof typeof mastery;
    if (k in mastery) mastery[k]++;
  }
  const today = new Date().toISOString().slice(0, 10);
  const dueToday = graph.nodes.reduce(
    (acc, n) => acc + (n.next_review && n.next_review <= today ? 1 : 0),
    0,
  );

  const p = resolve(DOCS, 'index.md');
  const fm = existsSync(p)
    ? (matter(readFileSync(p, 'utf-8')).data as Record<string, unknown>)
    : {};

  return {
    pages: graph.nodes.length,
    orphans: Number(fm.orphans ?? 0),
    conflicts: Number(fm.conflicts ?? 0),
    dueToday,
    mastery,
    // 'ok' 는 비교용 센티넬(Header/HealthCards 가 === 'ok' 로 색 분기) — 유지.
    // 비-ok 표시 문자열만 한글화(영문 'cycles' 제거).
    dagIntegrity: (graph.stats?.cycles ?? 0) === 0 ? 'ok' : `${graph.stats.cycles}개 순환`,
    suggestedAction: String(fm.suggested_action ?? ''),
    lastUpdated: String(fm.last_updated ?? ''),
  };
}

export type LogEntry = { date: string; operation: string; subject: string; raw: string };

export function readLog(limit?: number): LogEntry[] {
  const p = resolve(DOCS, 'log.md');
  if (!existsSync(p)) return [];
  const text = readFileSync(p, 'utf-8');
  const entries: LogEntry[] = [];
  for (const m of text.matchAll(/^## \[(\d{4}-\d{2}-\d{2})\]\s*([^|]+?)\s*\|\s*(.*)$/gm)) {
    entries.push({ date: m[1], operation: m[2].trim(), subject: m[3].trim(), raw: m[0] });
  }
  entries.reverse();
  return limit ? entries.slice(0, limit) : entries;
}

// 로그 subject 의 raw 슬러그 경로(예: logic/high-1/집합과_명제/논리, 2023/6월모평/2023_6월모평_미적분_30)를
// 사람이 읽는 leaf 라벨(논리 / 2023 6월모평 미적분 30)로 치환. 활동 피드·/log 의 슬래시 경로 노출 제거.
const _LOG_PATH_RE = /(?:[\w가-힣-]+\/)+[\w가-힣-]+/g;
export function cleanLogSubject(subject: string): string {
  if (!subject) return subject;
  return subject.replace(_LOG_PATH_RE, (m) => {
    const leaf = m.split('/').filter(Boolean).pop() ?? m;
    return leaf.replace(/_/g, ' ');
  });
}

// 사용자에게 의미 있는 학습 활동 op(노트 promote). 그 외(prune/restructure/ingest/init/env/merge/deploy/
// curriculum/fix 등)는 개발·운영 작업이라 비관리자 피드에서 제외.
export const USER_ACTIVITY_OPS = ['promote'];

export type ConceptGraph = {
  generatedAt: string;
  nodes: Array<{
    id: string; slug: string; label: string;
    concept_type: string; mastery: string;
    grade?: string; domain?: string; unit?: string; home_unit?: string;
    prerequisites: string[]; enables: string[];
    review_state: string | null; next_review: string | null;
    x: number; y: number;
  }>;
  edges: Array<{ id: string; source: string; target: string }>;
  stats: {
    nodes: number; edges: number; cycles: number;
    byMastery: Record<string, number>;
    byType: Record<string, number>;
  };
};

export function readConceptGraph(): ConceptGraph {
  const p = resolve(WEB_ROOT, 'src', 'data', 'concept-graph.json');
  if (!existsSync(p)) {
    return { generatedAt: '', nodes: [], edges: [], stats: { nodes: 0, edges: 0, cycles: 0, byMastery: {}, byType: {} } };
  }
  return JSON.parse(readFileSync(p, 'utf-8'));
}

// 개념별 문제참조 수 — 진행도 "핵심개념(core)" 판정에 쓰는 중요도 신호.
// build-problem-index 가 만드는 정적 JSON(byConcept[id] = 그 개념을 다루는 문제 엔트리 배열).
// 모듈 1회 캐시: 빌드 산출물이라 런타임 불변 → SSR 매 요청·멤버마다 재파싱 방지(content 변경 시 server restart 로 갱신).
let _problemRefByConcept: Record<string, unknown[]> | null = null;
function problemRefCount(conceptId: string): number {
  if (_problemRefByConcept === null) {
    const p = resolve(WEB_ROOT, 'src', 'data', 'problems-by-concept.json');
    _problemRefByConcept = existsSync(p)
      ? ((JSON.parse(readFileSync(p, 'utf-8')).byConcept as Record<string, unknown[]>) ?? {})
      : {};
  }
  const v = _problemRefByConcept[conceptId];
  return Array.isArray(v) ? v.length : 0;
}

// ---- 단원(unit) 중심 진행도 ------------------------------------------------
// 스포크(정의/정리/예제) mastery 를 home_unit 기준으로 49개 단원에 롤업한다.
// 진행도 분모는 전체 스포크(최대 175)가 아니라 단원의 "핵심개념"만 — 인제스트가 양산한
// 문제참조 0 근사중복 정의를 빼서, 기출 핵심을 익히면 100% 도달이 실제로 가능하게 한다.
// (computeUnitProgress 의 Core-Coverage-at-Threshold 산식 참고.)
type GNode = ConceptGraph['nodes'][number];

export type UnitStatus = 'unknown' | 'learning' | 'proficient' | 'mastered';

export type UnitProgress = {
  unitId: string;
  label: string;
  grade?: string;
  domain?: string;
  spokeCount: number;
  mastery: { unknown: number; learning: number; proficient: number; mastered: number };
  progressPercent: number;
  // 심화축(stretch goal) — 단원의 *모든* 멤버를 mastered 까지 올린 비율(구 진행율 산식값).
  // 메인 progressPercent 가 '핵심 이수율'로 바뀌면서, '전부 제패'는 이 보조축으로 보존.
  depthPercent?: number;
  status: UnitStatus;
};

const MASTERY_POINTS: Record<string, number> = { unknown: 0, learning: 1, proficient: 2, mastered: 3 };

// progress% → 4단계 status. 임계값은 여기서 튜닝.
function progressToStatus(pct: number): UnitStatus {
  if (pct >= 100) return 'mastered';
  if (pct >= 50) return 'proficient';
  if (pct > 0) return 'learning';
  return 'unknown';
}

// 49개 단원 각각의 진행도. 멤버 = 그 단원의 스포크 + 단원 노드 자신.
// masteryOf: 멀티유저에서 사용자별 mastery 를 주입하는 resolver(없으면 그래프 전역값).
export function computeUnitProgress(masteryOf?: (conceptId: string) => UnitStatus): UnitProgress[] {
  const graph = readConceptGraph();
  const units = graph.nodes.filter((n) => n.concept_type === 'unit');
  const membersByUnit = new Map<string, GNode[]>();
  for (const u of units) membersByUnit.set(u.id, [u]); // 단원 노드 자신 포함
  for (const n of graph.nodes) {
    if (n.concept_type === 'unit') continue;
    const home = n.home_unit;
    if (home && membersByUnit.has(home)) membersByUnit.get(home)!.push(n);
  }
  const lvlOf = (m: GNode): UnitStatus => (masteryOf ? masteryOf(m.id) : (m.mastery as UnitStatus));
  return units.map((u) => {
    const members = membersByUnit.get(u.id)!;
    const mastery = { unknown: 0, learning: 0, proficient: 0, mastered: 0 };
    let points = 0;
    for (const m of members) {
      const lvl = lvlOf(m);
      if (lvl in mastery) mastery[lvl]++;
      points += MASTERY_POINTS[lvl] ?? 0;
    }
    // ── 진행도 = 단원의 "핵심개념" 중 proficient 이상 이수 비율(Core-Coverage-at-Threshold).
    // 핵심(core) = 단원 노드 + 문제참조≥1 spoke + 모든 정리(theorem). 인제스트가 양산한
    // 문제참조 0 근사중복 정의(전체 spoke 의 28%)는 분모에서 빠져 100% 천장을 막지 않는다.
    // 100% = "기출에 나오는 핵심개념을 모두 proficient 이상으로 이수". (모든 미세 정의까지
    // mastered 요구하던 구 모델은 아래 depthPercent 심화축으로 보존.)
    const isCore = (m: GNode) =>
      m.concept_type === 'unit' || m.concept_type === 'theorem' || problemRefCount(m.id) >= 1;
    // degrade: 문제참조 spoke 가 하나도 없는 단원(중등 일부 미태깅)은 핵심집합이 단원노드뿐이라
    // 단원만 찍어도 100% 되는 trivial-100 위험 → core=members 전체로 강등해 정직하게 만든다.
    const hasRefSpoke = members.some((m) => m.concept_type !== 'unit' && problemRefCount(m.id) >= 1);
    const core = hasRefSpoke ? members.filter(isCore) : members; // 단원 노드 항상 포함 → core.length≥1
    const covered = core.filter((m) => (MASTERY_POINTS[lvlOf(m)] ?? 0) >= 2).length; // proficient+ = 이수
    let progressPercent = core.length > 0 ? Math.round((covered / core.length) * 100) : 0;
    // started-floor: 어떤 멤버든 learning+ 면 round 결과가 0이어도 1%로 띄운다. all-unknown ⟺ pct=0
    // 등가를 보장 — 거대단원(최대 175 멤버)에서 단일 학습이 round→0으로 묻혀 started(pct>0)·atlas
    // locked·continuing 분기가 깨지는 회귀를 차단.
    const anyActive = members.some((m) => (MASTERY_POINTS[lvlOf(m)] ?? 0) >= 1);
    if (anyActive && progressPercent === 0) progressPercent = 1;
    if (!anyActive) progressPercent = 0;
    // 심화축(전부 mastered stretch goal) — 구 진행율 산식값. 카드 툴팁 등 옵셔널 표시용.
    const depthPercent = members.length > 0 ? Math.round((points / (members.length * 3)) * 100) : 0;
    // 단원 status = 단원 노드 자신의 mastery 와 spoke 평균 status 중 **높은 쪽**.
    // 사용자가 단원을 직접 능숙/숙달로 표시(튜터 promote)해도 spoke 평균만 쓰면,
    // 미학습 하위개념 수십 개에 묻혀 progressPercent≈1% → unknown 으로 떨어진다.
    // → 직접 표시한 능숙이 통계·지도에 전혀 반영 안 되는 버그. self 레벨로 끌어올린다.
    // (progressPercent 는 '하위개념 완성도'라 spoke 평균 유지 — status 와는 다른 축.)
    const selfLevel = lvlOf(u);
    const pctStatus = progressToStatus(progressPercent);
    const status: UnitStatus =
      (MASTERY_POINTS[selfLevel] ?? 0) >= (MASTERY_POINTS[pctStatus] ?? 0) ? selfLevel : pctStatus;
    return {
      unitId: u.id,
      label: u.label,
      grade: u.grade,
      domain: u.domain,
      spokeCount: members.length - 1,
      mastery,
      progressPercent,
      depthPercent,
      status,
    };
  });
}

export type UnitSummary = {
  total: number;
  started: number; // progress > 0% 인 단원 수
  byStatus: { unknown: number; learning: number; proficient: number; mastered: number };
};

// 헤더/대시보드 도넛용 단원 요약 (분모 = 단원 51).
export function unitSummary(masteryOf?: (conceptId: string) => UnitStatus): UnitSummary {
  const units = computeUnitProgress(masteryOf);
  const byStatus = { unknown: 0, learning: 0, proficient: 0, mastered: 0 };
  let started = 0;
  for (const u of units) {
    byStatus[u.status]++;
    if (u.progressPercent > 0) started++;
  }
  return { total: units.length, started, byStatus };
}

// 학년 정렬 키. atlas.ts 의 도메인 내 phyllotaxis 배치도 이 순위를 재사용한다.
export const GRADE_RANK: Record<string, number> = {
  '중1': 1, '중2': 2, '중3': 3, '고1': 4, '수학1': 5, '수학2': 6, '미적분': 7, '기하': 7, '확률과통계': 7,
};

// /concepts 상단 진행도 섹션용 추천.
//  - continuing: 진행 중(0<진행<100), 진행률 높은 순.
//  - ready: 미착수(0%) & 모든 선수 단원이 능숙+ (선수 없는 root = "여기서 시작"), 기초 학년 우선.
//  - review: next_review ≤ 오늘인 개념을 가진 단원.
export function recommendUnits(masteryOf?: (conceptId: string) => UnitStatus): { continuing: UnitProgress[]; ready: UnitProgress[]; review: UnitProgress[] } {
  const graph = readConceptGraph();
  const units = computeUnitProgress(masteryOf);
  const byId = new Map(units.map((u) => [u.unitId, u]));
  const prereqOf = new Map(
    graph.nodes.filter((n) => n.concept_type === 'unit').map((n) => [n.id, n.prerequisites ?? []]),
  );

  const today = new Date().toISOString().slice(0, 10);
  const dueUnits = new Set<string>();
  for (const n of graph.nodes) {
    if (n.next_review && n.next_review <= today) {
      const home = n.home_unit ?? (n.concept_type === 'unit' ? n.id : undefined);
      if (home) dueUnits.add(home);
    }
  }

  // 시작한 단원 중 복습 도래분만 review, 나머지 진행 중은 continuing (상호 배타).
  const review = units
    .filter((u) => u.progressPercent > 0 && dueUnits.has(u.unitId))
    .sort((a, b) => b.progressPercent - a.progressPercent);
  const continuing = units
    .filter((u) => u.progressPercent > 0 && u.progressPercent < 100 && !dueUnits.has(u.unitId))
    .sort((a, b) => b.progressPercent - a.progressPercent);

  const ready = units
    .filter((u) => {
      if (u.progressPercent > 0) return false;
      const prereqUnits = (prereqOf.get(u.unitId) ?? []).filter((p) => byId.has(p));
      return prereqUnits.every((p) => {
        const s = byId.get(p)!.status;
        return s === 'proficient' || s === 'mastered';
      });
    })
    .sort((a, b) => (GRADE_RANK[a.grade ?? ''] ?? 9) - (GRADE_RANK[b.grade ?? ''] ?? 9) || a.label.localeCompare(b.label, 'ko-KR'));

  return { continuing, ready, review };
}
