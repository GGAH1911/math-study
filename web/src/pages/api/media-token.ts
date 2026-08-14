// 단수명 미디어 토큰 발급 — POST /api/media-token
//   → 200 { token, expiresIn } · 401(미인증) · 503(비밀 미설정)
//
// Phase 5 에서 이미지가 R2/Worker 로 나가면 그쪽은 우리 세션 쿠키를 모른다. 웹/앱이 여기서
// 짧게 사는 토큰을 받아 Worker 에 제시하고, Worker 가 같은 비밀로 서명을 검증한다.
//
// ★지금은 **소비자가 없다**(Phase 5 에 생긴다). 순수 추가분이라 기존 인증 흐름을 건드리지 않는다 —
//   Phase 3 의 인증 항목 중 유일하게 "실패해도 로그인이 안 깨지는" 것이라 먼저 넣는다.
// ★GET 이 아니라 POST 다. 토큰이 URL 에 실리면 브라우저 히스토리·리퍼러·서버 로그에 남는다.
import type { APIRoute } from 'astro';
import { issueMediaToken, mediaTokenConfigured, MEDIA_TOKEN_TTL_SEC } from '../../lib/media-token.ts';

export const prerender = false;

const json = (body: unknown, status: number) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json', 'cache-control': 'no-store' },
  });

export const POST: APIRoute = async ({ locals }) => {
  // 미들웨어가 이미 세션을 해석해 locals.user 에 넣는다. 여기서 다시 풀지 않는다.
  const user = (locals as { user?: { id?: string } }).user;
  if (!user?.id) return json({ error: 'unauthorized' }, 401);

  if (!mediaTokenConfigured()) {
    // 폴백으로 약한 키를 만들지 않는다 — 조용히 약한 서명을 쓰는 게 발급 실패보다 나쁘다.
    console.error('[media-token] MS_MEDIA_JWT_SECRET 미설정(32자 이상 필요) — 발급 불가');
    return json({ error: 'media token not configured' }, 503);
  }

  const issued = issueMediaToken(user.id);
  if (!issued) return json({ error: 'issue failed' }, 503);
  return json({ token: issued.token, expiresIn: MEDIA_TOKEN_TTL_SEC }, 200);
};
