// 기출 상세 — `GET /api/problems/<slug>` → 화면이 그릴 전부(본문 HTML·메타·재구성·회차 네비)
//
// ★재구성(로제타 디코드 + Gemini 교정)은 **어드민 전용**이다. 그 판정을 서버에서 한다 —
//   클라이언트가 정하면 우회된다.
import type { APIRoute } from 'astro';
import { buildProblemDetail } from '../../../lib/problem-detail.ts';

export const prerender = false;

export const GET: APIRoute = async ({ params, locals }) => {
  const slug = String(params.slug ?? '');
  if (!slug) return new Response(JSON.stringify({ error: 'bad slug' }), { status: 400 });
  const isAdmin = !!(locals as { user?: { is_admin?: boolean } }).user?.is_admin;
  try {
    const d = await buildProblemDetail(slug, isAdmin);
    if (!d) return new Response(JSON.stringify({ error: 'not found' }), { status: 404 });
    return new Response(JSON.stringify(d), {
      status: 200,
      // 사용자별(admin 여부)로 내용이 갈리므로 공유 캐시에 남기지 않는다.
      headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
    });
  } catch (e) {
    console.error('[problem-detail]', e);
    return new Response(JSON.stringify({ error: 'detail failed' }), { status: 500 });
  }
};
