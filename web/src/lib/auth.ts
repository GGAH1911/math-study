// 인증 코어 — 비밀번호 해싱(scrypt)·DB 세션·CSRF(Origin)·로그인 레이트리밋.
// 보안 원칙:
//  - 비번은 crypto.scrypt(내장, 네이티브 의존성 0) + per-password salt + timingSafeEqual.
//  - 세션은 DB 백업: 쿠키엔 랜덤 토큰 원본, DB엔 sha256(token)만 → DB 유출돼도 위조 불가.
//  - 쿠키 HttpOnly·SameSite=Lax·(HTTPS 시)Secure. SameSite+Origin 검증으로 CSRF 방어.
//  - 로그인 실패는 auth_throttle 로 브루트포스 차단.
import type { AstroCookies } from 'astro';
import { scrypt as _scrypt, randomBytes, createHash, timingSafeEqual } from 'node:crypto';
import { promisify } from 'node:util';
import sql from './db.ts';
import { isAdminEmail } from './admin.ts';

const scrypt = promisify(_scrypt) as (
  password: string | Buffer, salt: string | Buffer, keylen: number,
  options: { N: number; r: number; p: number; maxmem?: number },
) => Promise<Buffer>;

export type User = {
  id: string;
  email: string;
  display_name: string | null;
  is_legacy: boolean;
  is_active: boolean;
  is_admin: boolean; // 이메일 allowlist 로 결정(DB 컬럼 아님). admin.ts 참조.
};

// ─────────────────────────────────────────── 비밀번호 (scrypt)
// N=2^14: 메모리 16MB/해시(기본 maxmem 32MB 내). 포맷에 파라미터 박아 추후 상향 가능.
const SCRYPT = { N: 16384, r: 8, p: 1, keylen: 64, maxmem: 64 * 1024 * 1024 };

export async function hashPassword(password: string): Promise<string> {
  const salt = randomBytes(16);
  const hash = await scrypt(password.normalize('NFKC'), salt, SCRYPT.keylen, SCRYPT);
  return `scrypt$${SCRYPT.N}$${SCRYPT.r}$${SCRYPT.p}$${salt.toString('hex')}$${hash.toString('hex')}`;
}

// 사용자 미존재 시에도 동일한 scrypt 비용을 치르게 해 타이밍 기반 계정 열거를 막는다.
// (login 에서 password_hash 가 없으면 이 더미 해시로 verifyPassword 를 돌린다.)
let _dummyHash: Promise<string> | null = null;
export function getDummyHash(): Promise<string> {
  if (!_dummyHash) _dummyHash = hashPassword(randomBytes(24).toString('hex'));
  return _dummyHash;
}

export async function verifyPassword(password: string, stored: string | null): Promise<boolean> {
  if (!stored) return false;
  try {
    const [scheme, ns, rs, ps, saltHex, hashHex] = stored.split('$');
    if (scheme !== 'scrypt' || !hashHex) return false;
    const N = parseInt(ns, 10), r = parseInt(rs, 10), p = parseInt(ps, 10);
    const salt = Buffer.from(saltHex, 'hex');
    const expected = Buffer.from(hashHex, 'hex');
    const actual = await scrypt(password.normalize('NFKC'), salt, expected.length, { N, r, p, maxmem: SCRYPT.maxmem });
    return actual.length === expected.length && timingSafeEqual(actual, expected);
  } catch {
    return false;
  }
}

// ─────────────────────────────────────────── 세션
export const SESSION_COOKIE = 'ms_session';
const SESSION_TTL_MS = 30 * 24 * 60 * 60 * 1000; // 30일
// 프로덕션(NODE_ENV=production)은 항상 Secure 쿠키(HTTPS 전제) — 깜빡 누락 방지. env로도 강제 가능.
const SECURE_COOKIES = process.env.MATH_STUDY_SECURE_COOKIES === 'true' || process.env.NODE_ENV === 'production';

function hashToken(token: string): string {
  return createHash('sha256').update(token).digest('hex');
}

export async function createSession(
  userId: string,
  meta: { userAgent?: string | null; ip?: string | null } = {},
): Promise<{ token: string; expiresAt: Date }> {
  const token = randomBytes(32).toString('base64url');
  const expiresAt = new Date(Date.now() + SESSION_TTL_MS);
  await sql`
    INSERT INTO sessions (user_id, token_hash, expires_at, user_agent, ip)
    VALUES (${userId}, ${hashToken(token)}, ${expiresAt}, ${meta.userAgent ?? null}, ${meta.ip ?? null})
  `;
  return { token, expiresAt };
}

export async function getUserBySessionToken(token: string | undefined | null): Promise<User | null> {
  if (!token) return null;
  const rows = await sql<Omit<User, 'is_admin'>[]>`
    SELECT u.id, u.email, u.display_name, u.is_legacy, u.is_active
    FROM sessions s JOIN users u ON u.id = s.user_id
    WHERE s.token_hash = ${hashToken(token)} AND s.expires_at > NOW() AND u.is_active = TRUE
    LIMIT 1
  `;
  const u = rows[0];
  return u ? { ...u, is_admin: isAdminEmail(u.email) } : null;
}

export async function destroySession(token: string | undefined | null): Promise<void> {
  if (!token) return;
  await sql`DELETE FROM sessions WHERE token_hash = ${hashToken(token)}`;
}

export async function destroyAllUserSessions(userId: string): Promise<void> {
  await sql`DELETE FROM sessions WHERE user_id = ${userId}`;
}

export function setSessionCookie(cookies: AstroCookies, token: string, expiresAt: Date): void {
  cookies.set(SESSION_COOKIE, token, {
    httpOnly: true,
    sameSite: 'lax',
    secure: SECURE_COOKIES,
    path: '/',
    expires: expiresAt,
  });
}

export function clearSessionCookie(cookies: AstroCookies): void {
  cookies.delete(SESSION_COOKIE, { path: '/' });
}

export async function resolveUser(cookies: AstroCookies): Promise<User | null> {
  return getUserBySessionToken(cookies.get(SESSION_COOKIE)?.value);
}

// ─────────────────────────────────────────── CSRF (Origin/Referer 동일출처 검증)
// state-changing 요청(POST/PUT/PATCH/DELETE)에만 미들웨어가 적용.
export function isSameOrigin(request: Request): boolean {
  let host: string;
  try { host = new URL(request.url).host; } catch { return false; }
  const origin = request.headers.get('origin');
  if (origin) {
    try { return new URL(origin).host === host; } catch { return false; }
  }
  const referer = request.headers.get('referer');
  if (referer) {
    try { return new URL(referer).host === host; } catch { return false; }
  }
  return false; // Origin·Referer 둘 다 없으면 CSRF 의심 → 거부(동일출처 fetch 는 Origin 보냄)
}

// ─────────────────────────────────────────── 로그인 레이트리밋 (auth_throttle)
const THROTTLE_MAX_FAILS = 8;
const THROTTLE_WINDOW_MS = 15 * 60 * 1000;
const THROTTLE_LOCK_MS = 15 * 60 * 1000;

export async function isThrottled(key: string): Promise<{ locked: boolean; retryAfterSec: number }> {
  const rows = await sql<{ locked_until: Date | null }[]>`
    SELECT locked_until FROM auth_throttle WHERE key = ${key}
  `;
  const lu = rows[0]?.locked_until ? new Date(rows[0].locked_until) : null;
  if (lu && lu.getTime() > Date.now()) {
    return { locked: true, retryAfterSec: Math.ceil((lu.getTime() - Date.now()) / 1000) };
  }
  return { locked: false, retryAfterSec: 0 };
}

export async function recordAuthFailure(key: string): Promise<void> {
  const rows = await sql<{ fail_count: number; first_fail_at: Date }[]>`
    SELECT fail_count, first_fail_at FROM auth_throttle WHERE key = ${key}
  `;
  const now = Date.now();
  let count = 1;
  let firstFail = new Date();
  if (rows[0]) {
    const within = now - new Date(rows[0].first_fail_at).getTime() < THROTTLE_WINDOW_MS;
    count = within ? rows[0].fail_count + 1 : 1;
    firstFail = within ? new Date(rows[0].first_fail_at) : new Date();
  }
  const lockedUntil = count >= THROTTLE_MAX_FAILS ? new Date(now + THROTTLE_LOCK_MS) : null;
  await sql`
    INSERT INTO auth_throttle (key, fail_count, first_fail_at, locked_until)
    VALUES (${key}, ${count}, ${firstFail}, ${lockedUntil})
    ON CONFLICT (key) DO UPDATE SET fail_count = ${count}, first_fail_at = ${firstFail}, locked_until = ${lockedUntil}
  `;
}

export async function clearAuthFailures(key: string): Promise<void> {
  await sql`DELETE FROM auth_throttle WHERE key = ${key}`;
}

// ─────────────────────────────────────────── 입력 검증
export function normalizeEmail(email: string): string {
  return String(email ?? '').trim().toLowerCase();
}

export function isValidEmail(email: string): boolean {
  return email.length <= 254 && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// null 이면 통과, 문자열이면 거부 사유.
export function validatePassword(pw: unknown): string | null {
  if (typeof pw !== 'string') return '비밀번호를 입력하세요.';
  if (pw.length < 8) return '비밀번호는 8자 이상이어야 합니다.';
  if (pw.length > 200) return '비밀번호가 너무 깁니다(200자 이하).';
  return null;
}

// 클라이언트 IP 추출. 기본은 위조 불가능한 소켓 peer(Astro clientAddress).
// X-Forwarded-For 는 클라이언트가 임의 지정 가능해 throttle 우회·표적 락아웃에 악용되므로,
// 신뢰 프록시 뒤일 때만(MATH_STUDY_TRUST_PROXY=true) 옵트인으로 사용한다.
export function clientIp(request: Request, clientAddress?: string | null): string | null {
  if (process.env.MATH_STUDY_TRUST_PROXY === 'true') {
    const xff = request.headers.get('x-forwarded-for');
    if (xff) return xff.split(',')[0].trim();
    const xr = request.headers.get('x-real-ip');
    if (xr) return xr;
  }
  return clientAddress ?? null;
}
