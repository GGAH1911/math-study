// 선렌더 콘텐츠 서빙 — `GET /api/content/<collection>/<id>` → `{id, collection, data, html}`
//
// ★인증: 이 경로는 `PUBLIC_PATHS` 에 없으므로 미들웨어가 **로그인을 요구한다**(미인증 → 401 JSON).
//   기출 본문은 유료화 전제라 이게 핵심이다. 방출물을 `public/` 이나 `dist/client/` 에 두면
//   정적 핸들러가 미들웨어보다 먼저 응답해 **게이팅이 조용히 꺼진다** — 2026-08-14 에 기출 이미지
//   5,774장이 정확히 그 이유로 무인증 노출됐다. 그래서 `web/private/` 에 두고 여기서만 읽어 준다.
//
// ★앱(Capacitor)은 베어러 토큰으로 온다. 미들웨어가 이미 베어러를 받으므로 이 라우트도 그대로 된다.
//
// ★ETag 를 준다 — 앱이 오프라인 캐시를 갱신할 때 바뀐 것만 받게 하려는 것이다. 콘텐츠는 5,852건
//   64MB 라, 전부 다시 받게 하면 앱이 못 쓴다.
import type { APIRoute } from 'astro';
import { statSync, readFileSync } from 'node:fs';
import { mediaPath } from '../../../lib/media-root.ts';

export const prerender = false;

const json = (body: unknown, status: number) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json', 'cache-control': 'no-store' },
  });

export const GET: APIRoute = async ({ params, request }) => {
  const rest = params.path;
  if (!rest) return json({ error: 'bad path' }, 400);

  // 경로 탈출 차단은 mediaPath 가 한다(인증과 별개 문제 — `%2e%2e` 로 레포 밖을 읽히면 안 된다).
  const abs = mediaPath(`/content/${rest}.json`);
  if (!abs) return json({ error: 'bad path' }, 400);

  let st;
  try { st = statSync(abs); } catch { return json({ error: 'not found' }, 404); }
  if (!st.isFile()) return json({ error: 'not found' }, 404);

  const etag = `W/"${st.size.toString(36)}-${st.mtimeMs.toString(36)}"`;
  if (request.headers.get('if-none-match') === etag) {
    return new Response(null, { status: 304, headers: { etag } });
  }

  let buf: Buffer;
  try { buf = readFileSync(abs); } catch { return json({ error: 'not found' }, 404); }
  return new Response(buf, {
    status: 200,
    headers: {
      'content-type': 'application/json; charset=utf-8',
      etag,
      // private — 공유 캐시(프록시)에 남으면 게이팅의 의미가 없다.
      'cache-control': 'private, max-age=300',
    },
  });
};
