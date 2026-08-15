// 작업 로그 — `GET /api/log` → `docs/log.md` 엔트리
//
// ★어드민 전용 경로다(`middleware.ts` 의 `ADMIN_PATHS` 에 `/log` 가 있다). 이 API 는
//   `/api/log` 라 그 목록에 안 걸리므로 **여기서 직접 막는다** — 안 그러면 어드민 게이팅이
//   페이지에만 남고 데이터는 열린다.
import type { APIRoute } from 'astro';
import { readLog, cleanLogSubject } from '../../lib/health.ts';

export const prerender = false;

export const GET: APIRoute = async ({ locals }) => {
  const user = (locals as { user?: { is_admin?: boolean } }).user;
  if (!user?.is_admin) {
    return new Response(JSON.stringify({ error: 'forbidden: admin only' }), { status: 403, headers: { 'content-type': 'application/json' } });
  }
  try {
    const entries = readLog().map((e) => ({ date: e.date, operation: e.operation, subject: cleanLogSubject(e.subject) }));
    return new Response(JSON.stringify({ entries }), {
      status: 200,
      headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
    });
  } catch (e) {
    console.error('[log]', e);
    return new Response(JSON.stringify({ error: 'log failed' }), { status: 500, headers: { 'content-type': 'application/json' } });
  }
};
