// 단수명 미디어 토큰(HS256 JWT) — Phase 3 항목. Phase 5 의 서명 URL 전제.
//
// ★무엇에 쓰나: 이미지가 R2/Worker 로 나가면 그쪽은 우리 세션 쿠키를 모른다. 그래서 웹/앱이
//   **짧게 사는 토큰**을 받아 Worker 에 제시하고, Worker 는 우리 비밀키로 서명을 검증해
//   그 사용자에게만 이미지를 준다. 지금은 발급만 있고 소비자는 Phase 5 에 생긴다 —
//   그래서 이 파일은 **순수 추가분**이고 기존 인증 흐름을 건드리지 않는다.
//
// ★왜 라이브러리를 안 쓰나: `auth.ts` 가 "네이티브 의존성 0"(node:crypto 만) 원칙으로 서 있다.
//   HS256 은 HMAC-SHA256 한 줄이라 jose/jsonwebtoken 을 끌어올 이유가 없다. 의존성이 하나
//   늘면 앱 번들·CI·공급망 감사가 같이 늘어난다.
//
// ★왜 짧게 사는가: 토큰이 URL 이나 로그에 남을 수 있다. 유출돼도 곧 죽도록 기본 5분이다.
//   갱신은 세션이 살아 있는 한 언제든 다시 받으면 된다.
import { createHmac, timingSafeEqual, randomUUID } from 'node:crypto';

/** 기본 수명 5분. 유출 시 피해 창을 좁힌다. */
export const MEDIA_TOKEN_TTL_SEC = 300;

/** 서명 비밀. **없으면 발급하지 않는다** — 폴백으로 약한 키를 만들어 쓰면 그게 더 나쁘다. */
function secret(): string | null {
  const s = process.env.MS_MEDIA_JWT_SECRET;
  return s && s.length >= 32 ? s : null;
}

export function mediaTokenConfigured(): boolean {
  return secret() !== null;
}

const b64url = (b: Buffer | string): string =>
  Buffer.from(b).toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');

const unb64url = (s: string): Buffer =>
  Buffer.from(s.replace(/-/g, '+').replace(/_/g, '/'), 'base64');

export type MediaClaims = {
  sub: string;      // user id
  scope: 'media';   // 용도 고정 — 다른 목적에 재사용되지 않게
  jti: string;      // 추적·폐기용 식별자
  iat: number;
  exp: number;
};

/** 발급. 비밀이 없으면 null(호출부가 503 을 준다). */
export function issueMediaToken(userId: string, ttlSec = MEDIA_TOKEN_TTL_SEC): { token: string; claims: MediaClaims } | null {
  const key = secret();
  if (!key) return null;
  const now = Math.floor(Date.now() / 1000);
  const claims: MediaClaims = { sub: userId, scope: 'media', jti: randomUUID(), iat: now, exp: now + ttlSec };
  const head = b64url(JSON.stringify({ alg: 'HS256', typ: 'JWT' }));
  const body = b64url(JSON.stringify(claims));
  const sig = b64url(createHmac('sha256', key).update(`${head}.${body}`).digest());
  return { token: `${head}.${body}.${sig}`, claims };
}

/**
 * 검증. 유효하면 claims, 아니면 null.
 *
 * ★서명 비교는 `timingSafeEqual` 로 한다 — 문자열 `===` 는 앞에서부터 비교해 실패 시점이
 *   달라지므로, 반복 요청으로 바이트를 하나씩 맞춰갈 수 있다(타이밍 공격).
 * ★알고리즘을 헤더에서 읽어 신뢰하지 않는다. `alg: none` 이나 RS256 으로 바꿔치기하는
 *   고전적 JWT 우회를 막으려면 **우리가 기대하는 알고리즘만** 받아야 한다.
 */
export function verifyMediaToken(token: string | null | undefined): MediaClaims | null {
  const key = secret();
  if (!key || !token) return null;
  const parts = token.split('.');
  if (parts.length !== 3) return null;
  const [head, body, sig] = parts;

  let alg: unknown;
  try { alg = (JSON.parse(unb64url(head).toString('utf8')) as { alg?: unknown }).alg; } catch { return null; }
  if (alg !== 'HS256') return null;

  const expect = createHmac('sha256', key).update(`${head}.${body}`).digest();
  const got = unb64url(sig);
  if (got.length !== expect.length || !timingSafeEqual(got, expect)) return null;

  let claims: MediaClaims;
  try { claims = JSON.parse(unb64url(body).toString('utf8')) as MediaClaims; } catch { return null; }
  if (claims.scope !== 'media' || !claims.sub) return null;
  if (typeof claims.exp !== 'number' || claims.exp <= Math.floor(Date.now() / 1000)) return null;
  return claims;
}
