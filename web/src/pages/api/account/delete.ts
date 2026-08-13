// POST /api/account/delete — 회원 탈퇴(계정·전 데이터 완전 삭제). PIPA 정보주체 삭제권.
//
// 현재 로그인 사용자(locals.user)의 user_id 로 연결된 모든 테이블 행 + users 행을
// 한 트랜잭션(sql.begin)으로 영구 삭제한다. 삭제 후 세션 쿠키를 제거한다.
//
// 보안:
//  - 미인증(locals.user 없음)이면 401.
//  - CSRF 는 미들웨어가 동일출처(Origin/Referer)를 검증하므로 별도 토큰 불필요.
//  - 비밀번호 계정은 body.password 재확인을 강제(오삭제·세션탈취 방어). OAuth 전용
//    계정(password_hash NULL)은 재확인할 비번이 없으므로 동일출처 + 세션만으로 진행.
//
// 삭제 대상(모두 user_id 스코핑, 0003 에서 ON DELETE CASCADE 지정됨 — 그래도 감사·
// 미래 비-CASCADE 테이블 대비해 자식→부모 순서로 명시 삭제):
//   sessions · concept_mastery · user_profile · chat_history ·
//   problem_state · problem_attempts → users.
//   auth_throttle 는 user_id FK 가 아니라 email/ip 키라 별도(베스트에포트)로 정리.
import type { APIRoute } from 'astro';
import sql from '../../../lib/db.ts';
import { clearSessionCookie, verifyPassword, normalizeEmail } from '../../../lib/auth.ts';

export const prerender = false;

function json(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data), { status, headers: { 'content-type': 'application/json' } });
}

export const POST: APIRoute = async ({ request, cookies, locals }) => {
  const user = locals.user;
  if (!user) return json({ error: 'unauthorized' }, 401);
  const userId = user.id;

  // 본문(선택). 비번 계정이면 password 재확인을 강제한다.
  let body: Record<string, unknown> = {};
  try {
    const ct = request.headers.get('content-type') ?? '';
    if (ct.includes('application/json')) body = (await request.json().catch(() => ({}))) as Record<string, unknown>;
  } catch { body = {}; }

  // 현재 계정의 password_hash 조회(비번 계정 여부 판정 + 재확인).
  const rows = await sql<{ password_hash: string | null; email: string }[]>`
    SELECT password_hash, email FROM users WHERE id = ${userId} LIMIT 1
  `;
  const row = rows[0];
  if (!row) {
    // 세션은 있는데 유저 행이 없음(경합 삭제 등) — 쿠키 정리 후 종료.
    clearSessionCookie(cookies);
    return json({ ok: true });
  }

  // 비밀번호 계정은 재확인 강제. OAuth 전용(password_hash NULL)은 비번이 없어 생략.
  if (row.password_hash) {
    const password = typeof body.password === 'string' ? body.password : '';
    if (!password) return json({ error: '비밀번호를 입력해 주세요.' }, 400);
    const ok = await verifyPassword(password, row.password_hash);
    if (!ok) return json({ error: '비밀번호가 올바르지 않습니다.' }, 401);
  }

  // 한 트랜잭션으로 전 데이터 + 계정 삭제(자식 → 부모 순서).
  try {
    await sql.begin(async (tx) => {
      await tx`DELETE FROM sessions        WHERE user_id = ${userId}`;
      await tx`DELETE FROM concept_mastery  WHERE user_id = ${userId}`;
      await tx`DELETE FROM user_profile     WHERE user_id = ${userId}`;
      await tx`DELETE FROM chat_history      WHERE user_id = ${userId}`;
      // 이미지 본문은 chat_images 에 따로 있다 — 참조가 문자열이라 FK 가 안 걸리므로 여기서 지운다.
      // 트랜잭션 밖에서 부르면 탈퇴는 됐는데 본문만 남는 상태가 생긴다.
      await tx`
        WITH refd AS (
          SELECT DISTINCT t.m[1] AS hash FROM chat_history c,
            LATERAL regexp_matches(c.messages::text, 'img:sha256:([0-9a-f]{64})', 'g') AS t(m)
        )
        DELETE FROM chat_images ci WHERE NOT EXISTS (SELECT 1 FROM refd r WHERE r.hash = ci.hash)
      `;
      await tx`DELETE FROM problem_state     WHERE user_id = ${userId}`;
      await tx`DELETE FROM problem_attempts  WHERE user_id = ${userId}`;
      await tx`DELETE FROM users             WHERE id = ${userId}`;
      // auth_throttle: user_id FK 아님(로그인 레이트리밋 키). 이 계정 이메일 락 흔적 정리.
      const emailKey = `login:${normalizeEmail(row.email)}`;
      await tx`DELETE FROM auth_throttle WHERE key = ${emailKey}`;
    });
  } catch (e) {
    return json({ error: '탈퇴 처리 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.' }, 500);
  }

  // 세션 쿠키 제거(DB 세션은 위에서 이미 삭제됨).
  clearSessionCookie(cookies);
  return json({ ok: true });
};
