// 항해 지도 — `GET /api/atlas` → 좌표·블롭·에지·항로·심도 + 레일 요약
//
// ★`buildAtlas` 는 난수 0 의 결정적 빌더지만 **개념 그래프 전체** 위에서 돈다. 클라이언트로
//   옮기면 그래프를 통째로 보내야 하고 같은 배치를 두 곳에서 계산하게 된다.
// ★사용자별(mastery·due·활동)이라 `no-store`.
import type { APIRoute } from 'astro';
import { buildAtlasOverview } from '../../lib/atlas-overview.ts';

export const prerender = false;

export const GET: APIRoute = async ({ locals }) => {
  const userId = (locals as { user?: { id?: string } }).user?.id ?? null;
  try {
    const d = await buildAtlasOverview(userId);
    return new Response(JSON.stringify(d), {
      status: 200,
      headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
    });
  } catch (e) {
    console.error('[atlas]', e);
    return new Response(JSON.stringify({ error: 'atlas failed' }), { status: 500, headers: { 'content-type': 'application/json' } });
  }
};
