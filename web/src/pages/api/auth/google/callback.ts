// GET /api/auth/google/callback — Google 리다이렉트 수신 → 토큰 교환 → 유저 find-or-create → 세션.
// state 대조(CSRF), email_verified 확인. 자격증명 미설정 시 503.
import type { APIRoute } from 'astro';
import sql from '../../../../lib/db.ts';
import { normalizeEmail, createSession, setSessionCookie, clientIp } from '../../../../lib/auth.ts';
import { claimLegacyDataIfFirst } from '../../../../lib/user-claim.ts';

export const prerender = false;

export const GET: APIRoute = async ({ url, cookies, request, redirect }) => {
  const clientId = process.env.GOOGLE_OAUTH_CLIENT_ID;
  const clientSecret = process.env.GOOGLE_OAUTH_CLIENT_SECRET;
  if (!clientId || !clientSecret) return new Response('Google 로그인 미설정', { status: 503 });

  const code = url.searchParams.get('code');
  const state = url.searchParams.get('state');
  const savedState = cookies.get('ms_oauth_state')?.value;
  cookies.delete('ms_oauth_state', { path: '/' });
  if (!code || !state || !savedState || state !== savedState) {
    return new Response('OAuth state 불일치(만료 또는 위조)', { status: 400 });
  }

  const redirectUri = process.env.GOOGLE_OAUTH_REDIRECT_URI ?? `${url.origin}/api/auth/google/callback`;

  // 1) code → tokens
  const tokenRes = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      code, client_id: clientId, client_secret: clientSecret,
      redirect_uri: redirectUri, grant_type: 'authorization_code',
    }),
  });
  if (!tokenRes.ok) return new Response('토큰 교환 실패', { status: 502 });
  const tokens = (await tokenRes.json()) as { access_token?: string };
  if (!tokens.access_token) return new Response('토큰 없음', { status: 502 });

  // 2) userinfo
  const uiRes = await fetch('https://openidconnect.googleapis.com/v1/userinfo', {
    headers: { authorization: `Bearer ${tokens.access_token}` },
  });
  if (!uiRes.ok) return new Response('userinfo 실패', { status: 502 });
  const ui = (await uiRes.json()) as { sub?: string; email?: string; email_verified?: boolean; name?: string };
  if (!ui.sub || !ui.email) return new Response('Google 프로필 불완전', { status: 502 });
  // email_verified 를 양성 조건으로 강제(undefined/누락도 거부) — 미검증 이메일 신뢰 금지.
  if (ui.email_verified !== true) return new Response('Google 이메일 미인증', { status: 403 });

  const email = normalizeEmail(ui.email);
  const sub = String(ui.sub);

  // 3) find-or-create: (provider, subject) 매칭만 자동 로그인. 이미 가입된 이메일에는
  //    자동 링크하지 않는다(소유증명 없는 OAuth 자동링크 = 계정탈취 벡터).
  let user = (await sql<{ id: string }[]>`SELECT id FROM users WHERE oauth_provider = 'google' AND oauth_subject = ${sub} LIMIT 1`)[0];
  if (!user) {
    const byEmail = (await sql<{ id: string }[]>`SELECT id FROM users WHERE lower(email) = lower(${email}) LIMIT 1`)[0];
    if (byEmail) {
      // 비번 등으로 이미 존재 → 자동 링크 거부. 로그인 후 설정에서 명시적 연동해야 안전.
      return new Response('이미 가입된 이메일입니다. 비밀번호로 로그인하거나, 로그인 후 설정에서 Google 연동하세요.', { status: 409 });
    }
    user = (await sql<{ id: string }[]>`
      INSERT INTO users (email, oauth_provider, oauth_subject, display_name)
      VALUES (${email}, 'google', ${sub}, ${ui.name ?? null}) RETURNING id
    `)[0];
    try { await claimLegacyDataIfFirst(user.id); } catch (e) { console.error('[oauth] claim failed', e); }
  }

  const { token, expiresAt } = await createSession(user.id, {
    userAgent: request.headers.get('user-agent'), ip: clientIp(request),
  });
  setSessionCookie(cookies, token, expiresAt);
  await sql`UPDATE users SET last_login_at = NOW() WHERE id = ${user.id}`;
  return redirect('/', 302);
};
