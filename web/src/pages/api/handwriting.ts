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
  // ── 델타 동기화: `?since=<seq>` — 내 커서 이후에 바뀐 문서만 ──────────────────
  // ★필기는 문서 하나가 수십 KB 라 페이지마다 전부 받으면 앱에서 못 쓴다.
  //   기기 시계가 아니라 **서버 순번**으로 자른다(시계는 기기마다 어긋난다).
  const since = url.searchParams.get('since');
  if (since !== null) {
    const cursor = Number(since);
    if (!Number.isFinite(cursor) || cursor < 0) return json({ error: 'invalid since' }, 400);
    const rows = await sql<{ storage_key: string; doc: unknown; seq: string }[]>`
      SELECT storage_key, doc, seq FROM handwriting
       WHERE user_id = ${userId} AND seq > ${cursor}
       ORDER BY seq LIMIT 200
    `;
    const next = rows.length ? Number(rows[rows.length - 1].seq) : cursor;
    return json({ docs: rows.map((r) => ({ key: r.storage_key, doc: r.doc, seq: Number(r.seq) })),
                  cursor: next, more: rows.length === 200 });
  }

  const key = url.searchParams.get('key') ?? '';
  if (!KEY_RE.test(key)) return json({ error: 'invalid' }, 400);
  const rows = await sql<{ doc: unknown; seq: string | null }[]>`
    SELECT doc, seq FROM handwriting WHERE user_id = ${userId} AND storage_key = ${key} LIMIT 1
  `;
  return json({ doc: rows[0]?.doc ?? null, seq: rows[0]?.seq ? Number(rows[0].seq) : 0 });
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

  // 저장할 때마다 **서버가 순번을 새로 매긴다** — 그래야 다른 기기가 "이후 바뀐 것" 으로 잡는다.
  const [row] = await sql<{ seq: string }[]>`
    INSERT INTO handwriting (user_id, storage_key, doc, updated_at, seq)
    VALUES (${userId}, ${key}, ${sql.json(doc as never)}, NOW(), nextval('handwriting_seq'))
    ON CONFLICT (user_id, storage_key) DO UPDATE
      SET doc = ${sql.json(doc as never)}, updated_at = NOW(), seq = nextval('handwriting_seq')
    RETURNING seq
  `;
  return json({ ok: true, seq: Number(row.seq) });
};
