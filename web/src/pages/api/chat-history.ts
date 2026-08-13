// 대화 이력 계정화. GET 로 로드, POST 로 저장 (로그인 사용자별 · collection+slug 키).
import type { APIRoute } from 'astro';
import sql from '../../lib/db.ts';
import { externalizeImages, inflateImages } from '../../lib/chat-images.ts';

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
  const messages = rows[0]?.messages ?? [];
  // 저장은 참조('img:sha256:…')로 들어가 있다 — 클라이언트 계약대로 dataURL 로 되돌려 준다.
  return json({ messages: await inflateImages(messages) });
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
  // ★상한은 **인라인 원본** 기준으로 잰다. 참조로 바꾼 뒤에 재면 첨부가 아무리 많아도
  //   통과해 버려서 사실상 상한이 사라진다.

  // 이미지 본문을 chat_images 로 빼고 참조만 남긴다 — messages 는 매 턴 통째로 재기록되므로
  // 첨부가 안에 있으면 턴당 쓰기가 첨부 총량만큼 든다(대화 1건 568KB → 매 턴 568KB 재기록).
  const stored = await externalizeImages(messages);

  await sql`
    INSERT INTO chat_history (user_id, collection, slug, messages, updated_at)
    VALUES (${userId}, ${collection}, ${slug}, ${sql.json(stored as never)}, NOW())
    ON CONFLICT (user_id, collection, slug) DO UPDATE SET messages = ${sql.json(stored as never)}, updated_at = NOW()
  `;
  return json({ ok: true });
};
