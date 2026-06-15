// 학습 경로 생성 — 목표 개념까지의 미숙(능숙 미만) 선행 개념을 위상정렬해 학습 순서로.
// /paths 가 사용. 그래프는 사이클 0(build-concept-graph 가 보장)이라 DFS post-order 로 충분.
import type { ConceptGraph } from './health.ts';

export type PathStep = {
  id: string;
  label: string;
  domain: string | null;
  grade: string | null;
  concept_type: string;
  mastery: string;
  isGoal: boolean;
};

export type LearningPath = {
  goal: { id: string; label: string } | null;
  steps: PathStep[]; // 학습 순서(선행 먼저) — 미숙 선행 + 목표(마지막)
  totalPrereqs: number; // 전체 선행(이수 포함)
  donePrereqs: number; // 이미 능숙/숙달인 선행
  missingGoal: boolean; // goal id 가 그래프에 없음
};

// 이미 익혔다고 보는 단계 — 학습 경로에서 제외(목표 자신은 예외로 항상 포함).
const DONE = new Set(['proficient', 'mastered']);

export function buildLearningPath(
  graph: ConceptGraph,
  goalId: string,
  masteryOf: (id: string) => string,
): LearningPath {
  const byId = new Map(graph.nodes.map((n) => [n.id, n]));
  const goal = byId.get(goalId);
  if (!goal) return { goal: null, steps: [], totalPrereqs: 0, donePrereqs: 0, missingGoal: true };

  // DFS post-order: 선행을 모두 방문한 뒤 자신을 push → 선행이 항상 앞에 온다.
  const order: string[] = [];
  const visited = new Set<string>();
  const visit = (id: string) => {
    if (visited.has(id)) return;
    visited.add(id);
    const n = byId.get(id);
    if (!n) return;
    for (const pre of n.prerequisites ?? []) {
      if (byId.has(pre)) visit(pre);
    }
    order.push(id);
  };
  visit(goalId);

  const prereqIds = order.filter((id) => id !== goalId);
  const totalPrereqs = prereqIds.length;
  const donePrereqs = prereqIds.filter((id) => DONE.has(masteryOf(id))).length;

  const toStep = (id: string): PathStep => {
    const n = byId.get(id)!;
    return {
      id,
      label: n.label,
      domain: n.domain ?? null,
      grade: n.grade ?? null,
      concept_type: n.concept_type,
      mastery: masteryOf(id),
      isGoal: id === goalId,
    };
  };

  // 학습 시퀀스 = 미숙(능숙 미만) 선행 + 목표(마지막, 항상 포함).
  const steps = order
    .filter((id) => id === goalId || !DONE.has(masteryOf(id)))
    .map(toStep);

  return { goal: { id: goal.id, label: goal.label }, steps, totalPrereqs, donePrereqs, missingGoal: false };
}
