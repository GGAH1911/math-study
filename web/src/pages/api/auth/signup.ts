// POST /api/auth/signup  {email, password, displayName?}
// 계정 생성 → (첫 가입이면) 기존 single-user 데이터 상속 → 세션 발급.
import type { APIRoute } from 'astro';
import sql from '../../../lib/db.ts';
import {
  hashPassword, normalizeEmail, isValidEmail, validatePassword,
  createSession, setSessionCookie, clientIp, isThrottled, recordAuthFailure,
} from '../../../lib/auth.ts';
import { claimLegacyDataIfFirst } from '../../../lib/user-claim.ts';

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
  // 가입 레이트리밋(위조 불가 실제 IP) — scrypt(16MB/요청) 자원소진·계정스팸 방어. scrypt 전.
  const ip = clientIp(request, clientAddress);
  const ipKey = ip ? `ip:signup:${ip}` : null;
  if (ipKey) {
    const t = await isThrottled(ipKey);
    if (t.locked) return json({ error: `가입 시도가 너무 많습니다. ${t.retryAfterSec}초 후 다시 시도하세요.` }, 429);
    await recordAuthFailure(ipKey); // 매 시도 카운트(8회/15분 IP 상한)
  }

  const body = await readBody(request);
  const email = normalizeEmail(body.email ?? '');
  const password = body.password ?? '';
  const displayName = (body.displayName ?? body.display_name ?? '').trim().slice(0, 80) || null;

  if (!isValidEmail(email)) return json({ error: '유효한 이메일을 입력하세요.' }, 400);
  const pwErr = validatePassword(password);
  if (pwErr) return json({ error: pwErr }, 400);

  const dup = await sql`SELECT 1 FROM users WHERE lower(email) = lower(${email}) LIMIT 1`;
  if (dup.length) return json({ error: '이미 가입된 이메일입니다.' }, 409);

  const password_hash = await hashPassword(password);
  let user: { id: string; email: string; display_name: string | null };
  try {
    const rows = await sql<{ id: string; email: string; display_name: string | null }[]>`
      INSERT INTO users (email, password_hash, display_name)
      VALUES (${email}, ${password_hash}, ${displayName})
      RETURNING id, email, display_name
    `;
    user = rows[0];
  } catch {
    // lower(email) 유니크 인덱스 경합.
    return json({ error: '이미 가입된 이메일입니다.' }, 409);
  }

  // 첫 가입이면 기존 single-user 데이터 상속(실패해도 가입 자체는 성공시킨다).
  let claim = { claimed: false, reassignedState: 0, masterySeeded: 0 };
  try {
    claim = await claimLegacyDataIfFirst(user.id);
  } catch (e) {
    console.error('[signup] legacy claim failed:', e);
  }

  const { token, expiresAt } = await createSession(user.id, {
    userAgent: request.headers.get('user-agent'),
    ip,
  });
  setSessionCookie(cookies, token, expiresAt);
  await sql`UPDATE users SET last_login_at = NOW() WHERE id = ${user.id}`;

  return json({
    ok: true,
    user: { id: user.id, email: user.email, displayName: user.display_name },
    inherited: claim.claimed,
    inheritedState: claim.reassignedState,
    masterySeeded: claim.masterySeeded,
  });
};
