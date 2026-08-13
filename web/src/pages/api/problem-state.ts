// Read/write the learning state row for a single problem.
//
// GET  /api/problem-state?slug=...     → {state | null, recentAttempts: [...]}
// POST /api/problem-state              → {ok}
//   body: { slug, action: 'reset' | 'mark-mastered' | 'skip' }
import type { APIRoute } from 'astro';
import sql from '../../lib/db.ts';
import { recordEvent } from '../../lib/learning-events.ts';

export const prerender = false;

// sub-dir slug ('2025/수능/2025_수능_미적분_30') 허용. `..` / `\` 차단.
const SLUG_RE = /^[가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9_\-/]+$/;

// DB 의 frontmatter_path 는 여전히 `docs/problems/<basename>.md` (flat) 이므로
// sub-dir slug 가 들어오면 basename 만 추출해서 lookup.
function basenameOf(slug: string): string {
  return slug.split('/').pop() ?? slug;
}

async function findProblemId(slug: string): Promise<string | null> {
  const base = basenameOf(slug);
  const rows = await sql<{ id: string }[]>`
    SELECT id FROM problems WHERE frontmatter_path = ${`docs/problems/${base}.md`} LIMIT 1
  `;
  return rows[0]?.id ?? null;
}

export const GET: APIRoute = async ({ url, locals }) => {
  const userId = locals.user?.id;
  if (!userId) return j({ error: 'unauthorized' }, 401);
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
     WHERE user_id = ${userId} AND problem_id = ${pid}
  `;
  const recent = await sql<Array<{
    answer_given: string | null; is_correct: boolean | null;
    attempted_at: string; time_taken_sec: number | null; notes: string | null;
  }>>`
    SELECT answer_given, is_correct, attempted_at, time_taken_sec, notes
      FROM problem_attempts
     WHERE user_id = ${userId} AND problem_id = ${pid}
     ORDER BY attempted_at DESC LIMIT 5
  `;
  return j({ state: state ?? null, recentAttempts: recent });
};

export const POST: APIRoute = async ({ request, locals }) => {
  const userId = locals.user?.id;
  if (!userId) return j({ error: 'unauthorized' }, 401);
  let body: { slug: string; action: string; eventId?: string; occurredAt?: string };
  try { body = await request.json(); } catch { return j({ error: 'invalid json' }, 400); }
  const { slug, action, eventId, occurredAt } = body;
  if (!SLUG_RE.test(slug ?? '')) return j({ error: 'invalid slug' }, 400);
  const pid = await findProblemId(slug);
  if (!pid) return j({ error: 'problem not found' }, 404);

  // ★이벤트와 파생 상태를 **한 트랜잭션에서** 쓴다. 나누면 "이벤트는 남았는데 화면은 그대로"
  //   (또는 그 반대)가 생기고, 그게 정확히 재계산으로도 못 고치는 불일치다.
  //   `reset` 이 DELETE 인 게 핵심 이유다 — 시도 기록만 보고 재계산하면 지운 상태가 되살아난다.
  const meta = { eventId, occurredAt } as const;
  const ev = { userId, target: slug, payload: { problemId: pid }, ...meta };

  if (action === 'reset') {
    await sql.begin(async (tx) => {
      await recordEvent({ ...ev, kind: 'problem.reset' }, tx);
      await tx`DELETE FROM problem_state WHERE user_id = ${userId} AND problem_id = ${pid}`;
    });
    return j({ ok: true, action: 'reset' });
  }
  if (action === 'mark-mastered') {
    const next = new Date(Date.now() + 60 * 86_400_000).toISOString().slice(0, 10);
    await sql.begin(async (tx) => {
      await recordEvent({ ...ev, kind: 'problem.mark_mastered', payload: { problemId: pid, nextReview: next } }, tx);
      await tx`
        INSERT INTO problem_state (user_id, problem_id, status, review_state, next_review, last_attempted, attempt_count)
        VALUES (${userId}, ${pid}, 'solved', 'mature', ${next}, now(), 1)
        ON CONFLICT (user_id, problem_id) DO UPDATE SET
          status='solved', review_state='mature', next_review=EXCLUDED.next_review, last_attempted=now()
      `;
    });
    return j({ ok: true, action: 'mark-mastered' });
  }
  if (action === 'skip') {
    const next = new Date(Date.now() + 7 * 86_400_000).toISOString().slice(0, 10);
    await sql.begin(async (tx) => {
      await recordEvent({ ...ev, kind: 'problem.skip', payload: { problemId: pid, nextReview: next } }, tx);
      await tx`
        INSERT INTO problem_state (user_id, problem_id, status, review_state, next_review, last_attempted, attempt_count)
        VALUES (${userId}, ${pid}, 'review', 'new', ${next}, now(), 0)
        ON CONFLICT (user_id, problem_id) DO UPDATE SET next_review=EXCLUDED.next_review
      `;
    });
    return j({ ok: true, action: 'skip' });
  }
  return j({ error: 'unknown action' }, 400);
};

function j(p: unknown, s = 200): Response {
  return new Response(JSON.stringify(p), { status: s, headers: { 'Content-Type': 'application/json' } });
}
