// Read/write the learning state row for a single problem.
//
// GET  /api/problem-state?slug=...     → {state | null, recentAttempts: [...]}
// POST /api/problem-state              → {ok}
//   body: { slug, action: 'reset' | 'mark-mastered' | 'skip' }
import type { APIRoute } from 'astro';
import sql, { SINGLE_USER_ID } from '../../lib/db.ts';

export const prerender = false;

const SLUG_RE = /^[가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9_-]+$/;

async function findProblemId(slug: string): Promise<string | null> {
  const rows = await sql<{ id: string }[]>`
    SELECT id FROM problems WHERE frontmatter_path = ${`docs/problems/${slug}.md`} LIMIT 1
  `;
  return rows[0]?.id ?? null;
}

export const GET: APIRoute = async ({ url }) => {
  const slug = url.searchParams.get('slug') ?? '';
  if (!SLUG_RE.test(slug)) return j({ error: 'invalid slug' }, 400);
  const pid = await findProblemId(slug);
  if (!pid) return j({ error: 'problem not found' }, 404);

  const [state] = await sql<Array<{
    status: string; review_state: string;
    next_review: string | null; last_attempted: string | null; attempt_count: number;
  }>>`
    SELECT status, review_state, next_review, last_attempted, attempt_count
      FROM problem_state
     WHERE user_id = ${SINGLE_USER_ID} AND problem_id = ${pid}
  `;
  const recent = await sql<Array<{
    answer_given: string | null; is_correct: boolean | null;
    attempted_at: string; time_taken_sec: number | null; notes: string | null;
  }>>`
    SELECT answer_given, is_correct, attempted_at, time_taken_sec, notes
      FROM problem_attempts
     WHERE user_id = ${SINGLE_USER_ID} AND problem_id = ${pid}
     ORDER BY attempted_at DESC LIMIT 5
  `;
  return j({ state: state ?? null, recentAttempts: recent });
};

export const POST: APIRoute = async ({ request }) => {
  let body: { slug: string; action: string };
  try { body = await request.json(); } catch { return j({ error: 'invalid json' }, 400); }
  const { slug, action } = body;
  if (!SLUG_RE.test(slug ?? '')) return j({ error: 'invalid slug' }, 400);
  const pid = await findProblemId(slug);
  if (!pid) return j({ error: 'problem not found' }, 404);

  if (action === 'reset') {
    await sql`DELETE FROM problem_state WHERE user_id = ${SINGLE_USER_ID} AND problem_id = ${pid}`;
    return j({ ok: true, action: 'reset' });
  }
  if (action === 'mark-mastered') {
    const next = new Date(Date.now() + 60 * 86_400_000).toISOString().slice(0, 10);
    await sql`
      INSERT INTO problem_state (user_id, problem_id, status, review_state, next_review, last_attempted, attempt_count)
      VALUES (${SINGLE_USER_ID}, ${pid}, 'solved', 'mature', ${next}, now(), 1)
      ON CONFLICT (user_id, problem_id) DO UPDATE SET
        status='solved', review_state='mature', next_review=EXCLUDED.next_review, last_attempted=now()
    `;
    return j({ ok: true, action: 'mark-mastered' });
  }
  if (action === 'skip') {
    const next = new Date(Date.now() + 7 * 86_400_000).toISOString().slice(0, 10);
    await sql`
      INSERT INTO problem_state (user_id, problem_id, status, review_state, next_review, last_attempted, attempt_count)
      VALUES (${SINGLE_USER_ID}, ${pid}, 'review', 'new', ${next}, now(), 0)
      ON CONFLICT (user_id, problem_id) DO UPDATE SET next_review=EXCLUDED.next_review
    `;
    return j({ ok: true, action: 'skip' });
  }
  return j({ error: 'unknown action' }, 400);
};

function j(p: unknown, s = 200): Response {
  return new Response(JSON.stringify(p), { status: s, headers: { 'Content-Type': 'application/json' } });
}
