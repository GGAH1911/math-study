// 개념 상세 — `GET /api/concepts/<slug>` → 화면이 그릴 전부
//
// ★mastery 는 **로그인 사용자별**이라 `no-store` 다. 캐시되면 남의 진도가 보인다.
// ★flat-leaf 로 들어오면 404 대신 정식 경로를 알려 준다(라우트가 302 로 살리는 것과 같은 규칙).
import type { APIRoute } from 'astro';
import { buildConceptDetail, resolveConceptSlug } from '../../../lib/concept-detail.ts';

export const prerender = false;

const json = (b: unknown, s: number) =>
  new Response(JSON.stringify(b), { status: s, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' } });

export const GET: APIRoute = async ({ params, locals }) => {
  const slug = String(params.slug ?? '');
  if (!slug) return json({ error: 'bad slug' }, 400);
  const userId = (locals as { user?: { id?: string } }).user?.id ?? null;
  try {
    const d = await buildConceptDetail(slug, userId);
    if (d) return json(d, 200);
    const canonical = await resolveConceptSlug(slug);
    // 404 대신 정식 경로를 준다 — 클라이언트가 그쪽으로 이동한다.
    return canonical ? json({ error: 'moved', canonical }, 404) : json({ error: 'not found' }, 404);
  } catch (e) {
    console.error('[concept-detail]', e);
    return json({ error: 'detail failed' }, 500);
  }
};
