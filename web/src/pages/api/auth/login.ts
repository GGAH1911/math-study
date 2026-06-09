// POST /api/auth/login  {email, password}
// 레이트리밋 → 비번 검증(타이밍 안전) → 세션 발급. 계정 존재여부 노출 안 함.
import type { APIRoute } from 'astro';
import sql from '../../../lib/db.ts';
import {
  verifyPassword, getDummyHash, normalizeEmail,
  createSession, setSessionCookie, clientIp,
  isThrottled, recordAuthFailure, clearAuthFailures,
} from '../../../lib/auth.ts';

export const prerender = false;

function json(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data), { status, headers: { 'content-type': 'application/json' } });
}

async function readBody(request: Request): Promise<Record<string, string>> {
  const ct = request.headers.get('content-type') ?? '';
  if (ct.includes('application/json')) {
    return (await request.json().catch(() => ({}))) as Record<string, string>;
  }
  const fd = await request.formData();
  const o: Record<string, string> = {};
  for (const [k, v] of fd.entries()) o[k] = String(v);
  return o;
}

export const POST: APIRoute = async ({ request, cookies, clientAddress }) => {
  const body = await readBody(request);
  const email = normalizeEmail(body.email ?? '');
  const password = body.password ?? '';
  const ip = clientIp(request, clientAddress);
  // 락은 위조 불가능한 실제 소켓 IP 기준만. 이메일 단독 락은 표적 계정잠금 DoS 라 안 씀
  // (단일 IP 의 추측은 IP 락이, 비번경로는 dummy-hash 타이밍이 함께 방어).
  const ipKey = ip ? `ip:login:${ip}` : null;
  if (ipKey) {
    const ti = await isThrottled(ipKey);
    if (ti.locked) return json({ error: `시도가 너무 많습니다. ${ti.retryAfterSec}초 후 다시 시도하세요.` }, 429);
  }

  const rows = await sql<{ id: string; email: string; display_name: string | null; password_hash: string | null; is_active: boolean }[]>`
    SELECT id, email, display_name, password_hash, is_active FROM users WHERE lower(email) = lower(${email}) LIMIT 1
  `;
  const u = rows[0];

  // 타이밍 안전: 유저가 없어도 더미 해시로 동일 비용 지불(계정 열거 방지).
  const stored = u?.password_hash ?? (await getDummyHash());
  const passOk = await verifyPassword(password, stored);
  const ok = !!u && u.is_active && passOk;

  if (!ok) {
    if (ipKey) await recordAuthFailure(ipKey);
    return json({ error: '이메일 또는 비밀번호가 올바르지 않습니다.' }, 401);
  }

  if (ipKey) await clearAuthFailures(ipKey);

  const { token, expiresAt } = await createSession(u.id, {
    userAgent: request.headers.get('user-agent'),
    ip,
  });
  setSessionCookie(cookies, token, expiresAt);
  await sql`UPDATE users SET last_login_at = NOW() WHERE id = ${u.id}`;

  return json({ ok: true, user: { id: u.id, email: u.email, displayName: u.display_name } });
};
