// POST /api/auth/logout — 세션 폐기 + 쿠키 삭제.
import type { APIRoute } from 'astro';
import { SESSION_COOKIE, destroySession, clearSessionCookie } from '../../../lib/auth.ts';

export const prerender = false;

export const POST: APIRoute = async ({ cookies }) => {
  const token = cookies.get(SESSION_COOKIE)?.value;
  try { await destroySession(token); } catch { /* 이미 만료/없음 */ }
  clearSessionCookie(cookies);
  return new Response(JSON.stringify({ ok: true }), {
    status: 200,
    headers: { 'content-type': 'application/json' },
  });
};
