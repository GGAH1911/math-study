// 개념 대시보드 — `GET /api/concepts-overview` → 화면이 그릴 트리 전체
//
// ★이 화면은 목록이 아니라 **대시보드**다. 여섯 가지가 합쳐진다(사용자별 mastery·단원 진행도·
//   추천 3종·개념 요약·단원별 기출 수·위젯 유무). 클라이언트로 쪼개면 요청이 여섯 번 나가고,
//   단원↔스포크 매칭처럼 **파일 경로 의미에 기대는 로직**까지 브라우저로 옮겨야 한다.
//   그래서 서버가 **완성된 트리**를 한 번에 준다.
//
// ★사용자별 데이터가 섞이므로 `no-store` 다. 캐시되면 남의 진도가 보인다.
import type { APIRoute } from 'astro';
import { buildConceptsOverview } from '../../lib/concepts-overview.ts';

export const prerender = false;

export const GET: APIRoute = async ({ locals }) => {
  const user = (locals as { user?: { id?: string } }).user;
  try {
    const data = await buildConceptsOverview(user?.id ?? null);
    return new Response(JSON.stringify(data), {
      status: 200,
      headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
    });
  } catch (e) {
    console.error('[concepts-overview]', e);
    return new Response(JSON.stringify({ error: 'overview failed' }), {
      status: 500,
      headers: { 'content-type': 'application/json', 'cache-control': 'no-store' },
    });
  }
};
