// 그래프 패널 이력 계정화. GET 로 로드, POST 로 저장(로그인 사용자별 전역 롤링 배열).
// chat-history.ts 와 동일 패턴 — 단 collection/slug 없는 user 당 1행(entries 배열).
import type { APIRoute } from 'astro';
import sql from '../../lib/db.ts';

export const prerender = false;

const MAX_ENTRIES = 12;          // Graph.tsx HISTORY_MAX 와 일치
const MAX_BYTES = 2_000_000;     // 2MB cap

function json(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data), { status, headers: { 'content-type': 'application/json' } });
}

export const GET: APIRoute = async ({ locals }) => {
  const userId = locals.user?.id;
  if (!userId) return json({ error: 'unauthorized' }, 401);
  const rows = await sql<{ entries: unknown[] }[]>`
    SELECT entries FROM graph_history WHERE user_id = ${userId} LIMIT 1
  `;
  return json({ entries: rows[0]?.entries ?? [] });
};

export const POST: APIRoute = async ({ request, locals }) => {
  const userId = locals.user?.id;
  if (!userId) return json({ error: 'unauthorized' }, 401);
  let body: { entries?: unknown };
  try { body = (await request.json()) as typeof body; }
  catch { return json({ error: 'invalid json' }, 400); }

  const entries = body.entries;
  if (!Array.isArray(entries)) return json({ error: 'invalid' }, 400);
  const capped = entries.slice(-MAX_ENTRIES);
  if (JSON.stringify(capped).length > MAX_BYTES) return json({ error: 'payload too large' }, 413);

  await sql`
    INSERT INTO graph_history (user_id, entries, updated_at)
    VALUES (${userId}, ${sql.json(capped as never)}, NOW())
    ON CONFLICT (user_id) DO UPDATE SET entries = ${sql.json(capped as never)}, updated_at = NOW()
  `;
  return json({ ok: true });
};
