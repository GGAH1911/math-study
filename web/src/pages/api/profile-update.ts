// POST /api/profile-update  {goals?, self_reported_level?, learning_pace?, notes?, addWeaknesses?[]}
// 정성 학습자 프로필 갱신(로그인 사용자). 튜터가 학생 약점·목표·페이스를 파악하면 갱신.
import type { APIRoute } from 'astro';
import { upsertUserProfile, type ProfilePatch } from '../../lib/learner.ts';

export const prerender = false;

function json(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data), { status, headers: { 'content-type': 'application/json' } });
}

export const POST: APIRoute = async ({ request, locals }) => {
  const userId = locals.user?.id;
  if (!userId) return json({ error: 'unauthorized' }, 401);

  let body: Record<string, unknown>;
  try { body = (await request.json()) as Record<string, unknown>; }
  catch { return json({ error: 'invalid json' }, 400); }

  const patch: ProfilePatch = {};
  if (typeof body.goals === 'string') patch.goals = body.goals.slice(0, 500);
  if (typeof body.self_reported_level === 'string') patch.self_reported_level = body.self_reported_level.slice(0, 200);
  if (typeof body.learning_pace === 'string') patch.learning_pace = body.learning_pace.slice(0, 200);
  if (typeof body.notes === 'string') patch.notes = body.notes.slice(0, 2000);
  if (Array.isArray(body.addWeaknesses)) {
    patch.addWeaknesses = body.addWeaknesses
      .filter((w): w is string => typeof w === 'string')
      .slice(0, 10)
      .map((w) => w.slice(0, 300));
  }

  try {
    const profile = await upsertUserProfile(userId, patch);
    return json({ ok: true, profile });
  } catch (e) {
    return json({ error: (e as Error).message }, 500);
  }
};
