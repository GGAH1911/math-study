// 필기 캔버스 계정화. GET?key= 로 로드, POST {key, doc} 로 저장(로그인 사용자별·페이지별).
// chat-history.ts 패턴. key = InkCanvas storageKey ('problem:<id>' | 'concept:<id>' …).
import type { APIRoute } from 'astro';
import sql from '../../lib/db.ts';

export const prerender = false;

// storageKey 는 collection:slug 형태 — 한글·영숫자·_-/ 와 구분자 ':' 허용.
const KEY_RE = /^[가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9_\-/:]+$/;
const MAX_BYTES = 4_000_000;   // 4MB cap (필기는 스트로크 점 배열이라 큼)

function json(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data), { status, headers: { 'content-type': 'application/json' } });
}

export const GET: APIRoute = async ({ url, locals }) => {
  const userId = locals.user?.id;
  if (!userId) return json({ error: 'unauthorized' }, 401);
  const key = url.searchParams.get('key') ?? '';
  if (!KEY_RE.test(key)) return json({ error: 'invalid' }, 400);
  const rows = await sql<{ doc: unknown }[]>`
    SELECT doc FROM handwriting WHERE user_id = ${userId} AND storage_key = ${key} LIMIT 1
  `;
  return json({ doc: rows[0]?.doc ?? null });
};

export const POST: APIRoute = async ({ request, locals }) => {
  const userId = locals.user?.id;
  if (!userId) return json({ error: 'unauthorized' }, 401);
  let body: { key?: string; doc?: unknown };
  try { body = (await request.json()) as typeof body; }
  catch { return json({ error: 'invalid json' }, 400); }

  const { key, doc } = body;
  if (!key || !KEY_RE.test(key) || typeof doc !== 'object' || doc === null) {
    return json({ error: 'invalid' }, 400);
  }
  if (JSON.stringify(doc).length > MAX_BYTES) return json({ error: 'payload too large' }, 413);

  await sql`
    INSERT INTO handwriting (user_id, storage_key, doc, updated_at)
    VALUES (${userId}, ${key}, ${sql.json(doc as never)}, NOW())
    ON CONFLICT (user_id, storage_key) DO UPDATE SET doc = ${sql.json(doc as never)}, updated_at = NOW()
  `;
  return json({ ok: true });
};
