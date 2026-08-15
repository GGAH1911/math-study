// 컬렉션 목록 — `GET /api/content-index/<collection>` → `{collection, n, entries:[{id, …}]}`
//
// ★왜 별도 파일인가: 목록을 만들려고 요청마다 4,210개 파일을 읽을 수는 없다. 방출 시점에
//   컬렉션당 목록 한 벌을 굽고 여기서 그대로 내보낸다.
//
// ★목록에 담기는 필드는 방출기의 `LIST_FIELDS` 화이트리스트다. 문항 frontmatter 에는
//   `searchable_text`·`solution` 처럼 본문급으로 큰 필드가 있어 통째로 실으면 목록이 본문보다
//   커진다 — SPA 로 옮기는 이유가 사라진다.
//
// ★인증: `/api/content-index/` 는 `PUBLIC_PATHS` 에 없으므로 미인증은 401 이다. 목록도 콘텐츠다 —
//   문항이 몇 개 어떤 단원에 있는지는 그 자체로 상품 정보다.
import type { APIRoute } from 'astro';
import { statSync, readFileSync } from 'node:fs';
import { mediaPath } from '../../../lib/media-root.ts';

export const prerender = false;

/** 방출기의 `COLLECTIONS` 와 같아야 한다. 화이트리스트라 임의 파일명이 들어올 수 없다. */
const ALLOWED = new Set(['concepts', 'problems', 'mistakes', 'syntheses', 'tools']);

const json = (body: unknown, status: number) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json', 'cache-control': 'no-store' },
  });

export const GET: APIRoute = async ({ params, request }) => {
  const col = params.collection;
  if (!col || !ALLOWED.has(col)) return json({ error: 'unknown collection' }, 404);

  const abs = mediaPath(`/content/${col}.index.json`);
  if (!abs) return json({ error: 'bad path' }, 400);

  let st;
  try { st = statSync(abs); } catch {
    // 파일이 없다 = 방출을 안 돌렸다. 빈 목록을 주면 화면이 "문서 0건" 으로 조용히 비어
    // 원인을 찾기 어렵다. 503 으로 **무엇을 해야 하는지** 말한다.
    return json({ error: 'index not built', hint: 'node web/scripts/emit_content.mjs' }, 503);
  }

  const etag = `W/"${st.size.toString(36)}-${st.mtimeMs.toString(36)}"`;
  if (request.headers.get('if-none-match') === etag) {
    return new Response(null, { status: 304, headers: { etag } });
  }

  return new Response(readFileSync(abs), {
    status: 200,
    headers: {
      'content-type': 'application/json; charset=utf-8',
      etag,
      'cache-control': 'private, max-age=300',
    },
  });
};
