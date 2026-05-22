// Today's learning queue: every problem whose next_review ≤ today, ordered
// by oldest-due first. Brand-new problems (no problem_state row) are
// optionally included as the second batch so the queue never empties.
//
// GET /api/due-today?limit=20&includeNew=1
import type { APIRoute } from 'astro';
import sql, { SINGLE_USER_ID } from '../../lib/db.ts';

export const prerender = false;

type Row = {
  problem_id: string;
  frontmatter_path: string;
  unit_slug: string | null;
  killer_tier: string | null;
  subject: string;
  number: number;
  review_state: string | null;
  next_review: string | null;
  source: string;
};

export const GET: APIRoute = async ({ url }) => {
  const limit = Math.min(parseInt(url.searchParams.get('limit') ?? '20', 10) || 20, 100);
  const includeNew = url.searchParams.get('includeNew') !== '0';

  // Due rows first. The composite SELECT joins exams just to compose a
  // human-readable label ("2025 모의평가 9월" etc.).
  const due = await sql<Row[]>`
    SELECT p.id AS problem_id, p.frontmatter_path, p.unit_slug,
           p.killer_tier, p.subject, p.number,
           s.review_state, s.next_review,
           concat_ws(' ', e.year::text, e.exam_type, e.session, e.grade) AS source
      FROM problem_state s
      JOIN problems p ON p.id = s.problem_id
      JOIN exams e ON e.id = p.exam_id
     WHERE s.user_id = ${SINGLE_USER_ID}
       AND s.next_review IS NOT NULL
       AND s.next_review <= current_date
     ORDER BY s.next_review ASC, p.killer_tier NULLS LAST
     LIMIT ${limit}
  `;

  let neu: Row[] = [];
  if (includeNew && due.length < limit) {
    neu = await sql<Row[]>`
      SELECT p.id AS problem_id, p.frontmatter_path, p.unit_slug,
             p.killer_tier, p.subject, p.number,
             null::text AS review_state, null::date::text AS next_review,
             concat_ws(' ', e.year::text, e.exam_type, e.session, e.grade) AS source
        FROM problems p
        JOIN exams e ON e.id = p.exam_id
        LEFT JOIN problem_state s
               ON s.problem_id = p.id AND s.user_id = ${SINGLE_USER_ID}
       WHERE s.problem_id IS NULL
       ORDER BY e.year DESC, p.killer_tier ASC NULLS LAST, p.number ASC
       LIMIT ${limit - due.length}
    `;
  }

  return new Response(JSON.stringify({
    due: due.map(toCard),
    new: neu.map(toCard),
  }), { status: 200, headers: { 'Content-Type': 'application/json' } });
};

// slug regex 로 'YYYY_round_subject_N' → sub-dir path 'YYYY/round/YYYY_round_subject_N'
// 합성 (DB 는 flat path 유지 — Phase B 의 sub-dir migration 후 client URL 만 path-aware).
const SUBJECT_RE = /^(\d{4})_(.+)_(?:공통|기하|미적분|확률과통계|단일)_\d+$/;
function pathAwareSlug(flatSlug: string): string {
  const m = flatSlug.match(SUBJECT_RE);
  return m ? `${m[1]}/${m[2]}/${flatSlug}` : flatSlug;
}

function toCard(r: Row) {
  const flat = r.frontmatter_path.replace(/^docs\/problems\//, '').replace(/\.md$/, '');
  const slug = pathAwareSlug(flat);
  return {
    slug,
    href: `/problems/${slug}`,
    subject: r.subject,
    number: r.number,
    unit: r.unit_slug,
    tier: r.killer_tier,
    state: r.review_state,
    nextReview: r.next_review,
    source: r.source,
  };
}
