// 홈 대시보드 — `GET /api/home` → 화면이 그릴 전부
//
// ★사용자별(추천·연속학습일·mastery)이라 `no-store`.
// ★"오늘의 개념"은 KST 자정에 바뀐다 — 서버가 정한다(클라이언트 시계를 믿으면 기기마다 다르다).
import type { APIRoute } from 'astro';
import { buildHomeOverview } from '../../lib/home-overview.ts';

export const prerender = false;

export const GET: APIRoute = async ({ locals }) => {
  const userId = (locals as { user?: { id?: string } }).user?.id ?? null;
  try {
    const d = await buildHomeOverview(userId);
    return new Response(JSON.stringify(d), {
      status: 200,
      headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
    });
  } catch (e) {
    console.error('[home]', e);
    return new Response(JSON.stringify({ error: 'home failed' }), { status: 500, headers: { 'content-type': 'application/json' } });
  }
};
