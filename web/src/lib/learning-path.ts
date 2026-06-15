// 학습 경로 생성 — 목표 개념까지의 미숙(능숙 미만) 선행 개념을 *DAG* 로 반환.
// 선수관계는 1차원 시퀀스가 아니라 갈래가 합쳐지는 그래프 → 노드+엣지+층(layer)으로 낸다.
// /paths 의 MetroMap 이 세로 층상(위=기초 → 아래=목표 수렴)으로 렌더.
// 그래프는 사이클 0(build-concept-graph 보장)이라 DFS post-order = 유효 위상순서.
import type { ConceptGraph } from './health.ts';

export type PathNode = {
  id: string;
  label: string;
  domain: string | null;
  grade: string | null;
  concept_type: string;
  mastery: string;
  isGoal: boolean;
  isFrontier: boolean; // 미숙 서브그래프의 root = 지금 바로 배울 수 있는 개념
  layer: number;       // 0 = 기초(상단), 최대 = 목표(하단). 최장경로 층배정.
};

export type PathEdge = { from: string; to: string }; // 선수(from) → 의존(to), 둘 다 nodes 안

export type LearningPath = {
  goal: { id: string; label: string } | null;
  nodes: PathNode[]; // 미숙 선행 + 목표
  edges: PathEdge[];
  totalPrereqs: number; // 전체 선행(이수 포함)
  donePrereqs: number;  // 이미 능숙/숙달인 선행
  missingGoal: boolean;
};

// 이미 익혔다고 보는 단계 — 경로에서 제외(목표 자신은 예외로 항상 포함).
const DONE = new Set(['proficient', 'mastered']);

export function buildLearningPath(
  graph: ConceptGraph,
  goalId: string,
  masteryOf: (id: string) => string,
): LearningPath {
  const byId = new Map(graph.nodes.map((n) => [n.id, n]));
  const goal = byId.get(goalId);
  if (!goal) return { goal: null, nodes: [], edges: [], totalPrereqs: 0, donePrereqs: 0, missingGoal: true };

  // 모든 조상을 post-order(선행 먼저)로 수집.
  const order: string[] = [];
  const visited = new Set<string>();
  const visit = (id: string) => {
    if (visited.has(id)) return;
    visited.add(id);
    const n = byId.get(id);
    if (!n) return;
    for (const pre of n.prerequisites ?? []) if (byId.has(pre)) visit(pre);
    order.push(id);
  };
  visit(goalId);

  const prereqIds = order.filter((id) => id !== goalId);
  const totalPrereqs = prereqIds.length;
  const donePrereqs = prereqIds.filter((id) => DONE.has(masteryOf(id))).length;

  // 경로 노드 집합 = 미숙 선행 + 목표. (post-order 유지 → 위상순서)
  const inSet = (id: string) => id === goalId || !DONE.has(masteryOf(id));
  const setOrder = order.filter(inSet);
  const nodeSet = new Set(setOrder);

  // 집합 내 선수만 추린 인접(의존 노드별 in-set 선수 목록).
  const inPrereqs = (id: string): string[] =>
    (byId.get(id)?.prerequisites ?? []).filter((p) => nodeSet.has(p));

  // 엣지 = 집합 내 선수→의존.
  const edges: PathEdge[] = [];
  for (const id of setOrder) for (const p of inPrereqs(id)) edges.push({ from: p, to: id });

  // 층배정: 최장경로(roots=0 → 목표=최대). post-order 라 선수 layer 가 먼저 계산됨.
  const layer = new Map<string, number>();
  for (const id of setOrder) {
    const pres = inPrereqs(id);
    layer.set(id, pres.length ? Math.max(...pres.map((p) => layer.get(p) ?? 0)) + 1 : 0);
  }

  const nodes: PathNode[] = setOrder.map((id) => {
    const n = byId.get(id)!;
    return {
      id,
      label: n.label,
      domain: n.domain ?? null,
      grade: n.grade ?? null,
      concept_type: n.concept_type,
      mastery: masteryOf(id),
      isGoal: id === goalId,
      isFrontier: id !== goalId && inPrereqs(id).length === 0, // 미숙 선수 없음 = 지금 배울 수 있음
      layer: layer.get(id) ?? 0,
    };
  });

  return { goal: { id: goal.id, label: goal.label }, nodes, edges, totalPrereqs, donePrereqs, missingGoal: false };
}
