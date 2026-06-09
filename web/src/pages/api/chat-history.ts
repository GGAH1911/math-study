// 대화 이력 계정화. GET 로 로드, POST 로 저장 (로그인 사용자별 · collection+slug 키).
import type { APIRoute } from 'astro';
import sql from '../../lib/db.ts';

export const prerender = false;

const SLUG_RE = /^[가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9_\-/]+$/;
const COLLECTIONS = new Set(['concepts', 'problems', 'dashboard']);

function json(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data), { status, headers: { 'content-type': 'application/json' } });
}

export const GET: APIRoute = async ({ url, locals }) => {
  const userId = locals.user?.id;
  if (!userId) return json({ error: 'unauthorized' }, 401);
  const collection = url.searchParams.get('collection') ?? '';
  const slug = url.searchParams.get('slug') ?? '';
  if (!COLLECTIONS.has(collection) || !SLUG_RE.test(slug)) return json({ error: 'invalid' }, 400);
  const rows = await sql<{ messages: unknown[] }[]>`
    SELECT messages FROM chat_history WHERE user_id = ${userId} AND collection = ${collection} AND slug = ${slug} LIMIT 1
  `;
  return json({ messages: rows[0]?.messages ?? [] });
};

export const POST: APIRoute = async ({ request, locals }) => {
  const userId = locals.user?.id;
  if (!userId) return json({ error: 'unauthorized' }, 401);
  let body: { collection?: string; slug?: string; messages?: unknown };
  try { body = (await request.json()) as typeof body; }
  catch { return json({ error: 'invalid json' }, 400); }

  const { collection, slug, messages } = body;
  if (!collection || !COLLECTIONS.has(collection) || !slug || !SLUG_RE.test(slug) || !Array.isArray(messages)) {
    return json({ error: 'invalid' }, 400);
  }
  if (messages.length > 300) return json({ error: 'too many messages' }, 400);
  const jsonStr = JSON.stringify(messages);
  if (jsonStr.length > 2_000_000) return json({ error: 'payload too large' }, 413); // 2MB cap

  await sql`
    INSERT INTO chat_history (user_id, collection, slug, messages, updated_at)
    VALUES (${userId}, ${collection}, ${slug}, ${sql.json(messages as never)}, NOW())
    ON CONFLICT (user_id, collection, slug) DO UPDATE SET messages = ${sql.json(messages as never)}, updated_at = NOW()
  `;
  return json({ ok: true });
};
