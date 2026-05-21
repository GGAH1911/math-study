// Submit an attempt for a problem.
//   - Records problem_attempts row
//   - Computes is_correct against problems.answer via answersMatch()
//   - Promotes/demotes problem_state via nextSrsState() + UPSERTs the row
//
// POST /api/attempt
//   body: { slug: string, answer: string, timeTakenSec?: number, notes?: string }
//   200: { ok, correct, expected, nextReview, reviewState, intervalDays }
import type { APIRoute } from 'astro';
import sql, { SINGLE_USER_ID } from '../../lib/db.ts';
import { answersMatch, nextSrsState } from '../../lib/srs.ts';

export const prerender = false;

const SLUG_RE = /^[가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9_-]+$/;

type AttemptBody = {
  slug: string;
  answer: string;
  timeTakenSec?: number;
  notes?: string;
};

export const POST: APIRoute = async ({ request }) => {
  let body: AttemptBody;
  try { body = (await request.json()) as AttemptBody; }
  catch {
    return json({ error: 'invalid json' }, 400);
  }
  const { slug, answer, timeTakenSec, notes } = body;
  if (!slug || !SLUG_RE.test(slug)) return json({ error: 'invalid slug' }, 400);
  if (typeof answer !== 'string' || answer.length === 0 || answer.length > 200)
    return json({ error: 'invalid answer' }, 400);
  if (notes !== undefined && (typeof notes !== 'string' || notes.length > 2000))
    return json({ error: 'invalid notes' }, 400);
  if (timeTakenSec !== undefined &&
      (typeof timeTakenSec !== 'number' || timeTakenSec < 0 || timeTakenSec > 36000))
    return json({ error: 'invalid timeTakenSec' }, 400);

  // The problems.frontmatter_path stores `docs/problems/{slug}.md`.
  // We use that to find the row — slug uniquely identifies it.
  const rows = await sql<{ id: string; answer: string | null }[]>`
    SELECT id, answer
      FROM problems
     WHERE frontmatter_path = ${`docs/problems/${slug}.md`}
     LIMIT 1
  `;
  if (rows.length === 0) return json({ error: 'problem not found' }, 404);
  const problemId = rows[0].id;
  const expected = rows[0].answer ?? '';
  const correct = expected !== '' && answersMatch(answer, expected);

  // Current state (may not exist yet).
  const stateRows = await sql<{ review_state: 'new'|'learning'|'mature'; attempt_count: number }[]>`
    SELECT review_state, attempt_count
      FROM problem_state
     WHERE user_id = ${SINGLE_USER_ID} AND problem_id = ${problemId}
  `;
  const transition = nextSrsState(stateRows[0] ?? null, correct);

  // Record the attempt + upsert state in one transaction.
  await sql.begin(async (tx) => {
    await tx`
      INSERT INTO problem_attempts (user_id, problem_id, answer_given, is_correct, time_taken_sec, notes)
      VALUES (${SINGLE_USER_ID}, ${problemId}, ${answer},
              ${expected === '' ? null : correct},
              ${timeTakenSec ?? null}, ${notes ?? null})
    `;
    await tx`
      INSERT INTO problem_state
        (user_id, problem_id, status, review_state, next_review, last_attempted, attempt_count)
      VALUES
        (${SINGLE_USER_ID}, ${problemId}, ${transition.status},
         ${transition.reviewState}, ${transition.nextReview}, now(), 1)
      ON CONFLICT (user_id, problem_id) DO UPDATE SET
        status = EXCLUDED.status,
        review_state = EXCLUDED.review_state,
        next_review = EXCLUDED.next_review,
        last_attempted = now(),
        attempt_count = problem_state.attempt_count + 1
    `;
  });

  return json({
    ok: true,
    correct: expected === '' ? null : correct,
    expected: expected || null,
    nextReview: transition.nextReview,
    reviewState: transition.reviewState,
    intervalDays: transition.intervalDays,
  });
};

function json(payload: unknown, status = 200): Response {
  return new Response(JSON.stringify(payload), {
    status, headers: { 'Content-Type': 'application/json' },
  });
}
