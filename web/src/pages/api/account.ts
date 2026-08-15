// 내 정보 — `GET /api/account` → 계정·학습 현황·학습자 프로필
//
// ★비밀번호 **해시는 절대 내보내지 않는다.** 탈퇴 모달이 "비번 재확인이 필요한 계정인가"만
//   알면 되므로 `hasPassword` **불리언 하나**로 줄인다(OAuth 전용 계정은 비번이 없다).
// ★본인 데이터라 `no-store`.
import type { APIRoute } from 'astro';
import { getMasteryCounts } from '../../lib/mastery.ts';
import { getUserProfile } from '../../lib/learner.ts';
import sql from '../../lib/db.ts';

export const prerender = false;

export const GET: APIRoute = async ({ locals }) => {
  const user = (locals as { user?: { id?: string; email?: string; display_name?: string } }).user;
  if (!user?.id) {
    return new Response(JSON.stringify({ error: 'unauthorized' }), { status: 401, headers: { 'content-type': 'application/json' } });
  }
  try {
    const [counts, profile, pwRows] = await Promise.all([
      getMasteryCounts(user.id),
      getUserProfile(user.id),
      sql<{ has_password: boolean }[]>`
        SELECT (password_hash IS NOT NULL) AS has_password FROM users WHERE id = ${user.id} LIMIT 1`,
    ]);
    return new Response(JSON.stringify({
      user: { id: user.id, email: user.email, display_name: user.display_name },
      counts,
      recorded: counts.learning + counts.proficient + counts.mastered,
      profile,
      hasPassword: pwRows[0]?.has_password ?? false,
    }), { status: 200, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' } });
  } catch (e) {
    console.error('[account]', e);
    return new Response(JSON.stringify({ error: 'account failed' }), { status: 500, headers: { 'content-type': 'application/json' } });
  }
};
