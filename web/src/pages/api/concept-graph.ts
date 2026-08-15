// 개념 지도 데이터 — `GET /api/concept-graph` → mastery·노트수를 얹은 그래프
//
// ★그래프 원본은 1.4MB 다. 거기에 **사용자별 mastery** 와 **노트 개수**를 노드마다 얹어야 하므로
//   원본을 그대로 보내고 클라이언트가 합치게 하면 두 벌(그래프 + 상태)을 받게 된다.
//   서버가 합쳐 한 벌로 준다.
// ★사용자별이라 `no-store`.
import type { APIRoute } from 'astro';
import { readConceptGraph } from '../../lib/health.ts';
import { getMasteryMap } from '../../lib/mastery.ts';
import synthesesIndex from '../data/syntheses-by-concept.json';

export const prerender = false;

export const GET: APIRoute = async ({ locals }) => {
  const userId = (locals as { user?: { id?: string } }).user?.id ?? null;
  try {
    const graph = readConceptGraph();
    const masteryMap = userId ? await getMasteryMap(userId) : new Map<string, string>();
    const notesByConcept: Record<string, unknown[]> = (synthesesIndex as { byConcept?: Record<string, unknown[]> }).byConcept ?? {};
    return new Response(JSON.stringify({
      ...graph,
      nodes: graph.nodes.map((n: Record<string, unknown>) => ({
        ...n,
        mastery: masteryMap.get(String(n.id)) ?? 'unknown',
        note_count: notesByConcept[String(n.id)]?.length ?? 0,
      })),
    }), { status: 200, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' } });
  } catch (e) {
    console.error('[concept-graph]', e);
    return new Response(JSON.stringify({ error: 'graph failed' }), { status: 500, headers: { 'content-type': 'application/json' } });
  }
};
