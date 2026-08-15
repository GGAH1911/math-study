// 학습 경로 — `GET /api/learning-path?goal=<id>` → `{concepts, quickGoals, path}`
//
// ★그래프 알고리즘(위상정렬·선행 탐색)이 1.4MB `concept-graph.json` 위에서 돈다. 브라우저로
//   옮기면 그 파일을 통째로 보내야 하고, 규칙이 두 벌이 된다 — 서버가 계산해 결과만 준다.
// ★"미숙 선행" 판정은 **로그인 사용자의 mastery** 로 한다(전역 frontmatter 아님).
import type { APIRoute } from 'astro';
import { readConceptGraph, recommendUnits } from '../../lib/health.ts';
import { getMasteryMap } from '../../lib/mastery.ts';
import { buildLearningPath } from '../../lib/learning-path.ts';

export const prerender = false;

export const GET: APIRoute = async ({ url, locals }) => {
  const userId = (locals as { user?: { id?: string } }).user?.id ?? null;
  const goalId = url.searchParams.get('goal') ?? '';
  try {
    const graph = readConceptGraph();
    const masteryMap = userId ? await getMasteryMap(userId) : new Map<string, string>();
    const mof = (id: string) => (masteryMap.get(id) ?? 'unknown') as 'unknown' | 'learning' | 'proficient' | 'mastered';
    const path = goalId ? buildLearningPath(graph, goalId, mof) : null;
    const rec = recommendUnits(mof);

    return new Response(JSON.stringify({
      concepts: graph.nodes.map((n) => ({
        id: n.id, label: n.label, domain: n.domain ?? null, grade: n.grade ?? null, type: n.concept_type,
      })),
      // 빠른 진입용 예시 목표 = 진행 중·시작하기 좋은 단원.
      quickGoals: [...rec.continuing, ...rec.ready].slice(0, 6).map((u) => ({ id: u.unitId, label: u.label })),
      path: path && {
        goal: path.goal, missingGoal: path.missingGoal,
        totalPrereqs: path.totalPrereqs, donePrereqs: path.donePrereqs,
        nodes: path.nodes, edges: path.edges,
      },
    }), { status: 200, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' } });
  } catch (e) {
    console.error('[learning-path]', e);
    return new Response(JSON.stringify({ error: 'path failed' }), { status: 500, headers: { 'content-type': 'application/json' } });
  }
};
