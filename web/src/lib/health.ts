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
    dagIntegrity: (graph.stats?.cycles ?? 0) === 0 ? 'ok' : `${graph.stats.cycles} cycles`,
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

// ---- 단원(unit) 중심 진행도 ------------------------------------------------
// 스포크(정의/정리/예제) mastery 를 home_unit 기준으로 51개 단원에 롤업한다.
// 노드 단위(2789)는 달성 불가능한 분모라 진행도로 무의미 → 단원(51) 단위로.
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

// 51개 단원 각각의 진행도. 멤버 = 그 단원의 스포크 + 단원 노드 자신.
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
    const max = members.length * 3;
    const progressPercent = max > 0 ? Math.round((points / max) * 100) : 0;
    return {
      unitId: u.id,
      label: u.label,
      grade: u.grade,
      domain: u.domain,
      spokeCount: members.length - 1,
      mastery,
      progressPercent,
      status: progressToStatus(progressPercent),
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
