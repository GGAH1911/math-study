// GET /api/auth/google/start — Google OAuth 동의 화면으로 리다이렉트.
// 자격증명(GOOGLE_OAUTH_CLIENT_ID/SECRET)이 설정돼야 동작. 미설정 시 503.
import type { APIRoute } from 'astro';
import { randomBytes } from 'node:crypto';

export const prerender = false;
const SECURE = process.env.MATH_STUDY_SECURE_COOKIES === 'true';

export const GET: APIRoute = async ({ url, cookies, redirect }) => {
  const clientId = process.env.GOOGLE_OAUTH_CLIENT_ID;
  if (!clientId) {
    return new Response('Google 로그인이 아직 설정되지 않았습니다. (GOOGLE_OAUTH_CLIENT_ID 필요)', { status: 503 });
  }
  const redirectUri = process.env.GOOGLE_OAUTH_REDIRECT_URI ?? `${url.origin}/api/auth/google/callback`;

  // state: OAuth CSRF 방어 — 쿠키에 저장하고 callback 에서 대조.
  const state = randomBytes(16).toString('base64url');
  cookies.set('ms_oauth_state', state, { httpOnly: true, sameSite: 'lax', secure: SECURE, path: '/', maxAge: 600 });

  const authUrl = new URL('https://accounts.google.com/o/oauth2/v2/auth');
  authUrl.searchParams.set('client_id', clientId);
  authUrl.searchParams.set('redirect_uri', redirectUri);
  authUrl.searchParams.set('response_type', 'code');
  authUrl.searchParams.set('scope', 'openid email profile');
  authUrl.searchParams.set('state', state);
  authUrl.searchParams.set('access_type', 'online');
  authUrl.searchParams.set('prompt', 'select_account');
  return redirect(authUrl.toString(), 302);
};
