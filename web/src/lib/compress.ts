// 응답 gzip 압축 — 미들웨어가 나가는 길목에서 한 번만 감싼다.
//
// ★왜 필요한가 (2026-08-15 실측): 이 서버는 응답을 **전혀** 압축하지 않았다. `--compressed`
//   로 요청해도 2,379,804B 가 그대로 왔다(gzip 하면 244,638B — **9.7배**). Phase 3 이
//   SSR 껍데기를 ~200KB 로 줄였지만 그 200KB 도 무압축으로 나가고, API 응답은 더 크다.
//   모바일 데이터로 받게 하는 것이라 앱에서는 차이가 더 벌어진다.
//
// ★왜 여기(앱 안)인가: 로드맵은 "터널/프록시를 넣을 때 거기서 켜는 게 가장 싸다"고 적었고
//   그건 여전히 맞다 — 다만 **그 터널은 아직 없다**(Phase 5 미착수). 프록시가 생겨도 이
//   계층은 해가 없다: 프록시는 `content-encoding` 이 이미 붙은 응답을 다시 압축하지 않는다.
//   그때 이 파일을 지울지는 그때 재면 된다.
//
// ⚠️ **덮지 못하는 것 — 프로덕션 정적 자산**(`/_astro/*` 의 JS·CSS). node 어댑터(standalone)는
//   정적 파일을 미들웨어보다 **먼저** 응답하므로 이 계층에 닿지 않는다. dev(현재 tme 구성)에서는
//   Vite 가 같은 자리를 맡는다. 즉 여기서 줄어드는 것은 **SSR HTML 과 API 응답**이고, 번들은
//   터널/프록시가 생길 때 거기서 켜야 한다(Phase 5). 다 덮은 것처럼 읽히면 안 되므로 적어 둔다.

/**
 * 압축할 content-type **화이트리스트**.
 *
 * ★블랙리스트로 짜면 안 된다. `/api/chat` 은 `text/event-stream`(SSE)으로 튜터 토큰을
 *   흘리는데, 압축 스트림에 물리면 토큰이 버퍼에 갇혀 **화면에 늦게 뜬다.** 지금은 한 곳
 *   뿐이라 제외 목록으로도 되지만, 새 스트리밍 엔드포인트가 생기면 아무도 이 파일을
 *   고치지 않을 것이다 — 그때 조용히 느려진다. 새로 생긴 것은 **압축되지 않는 쪽**이
 *   기본값이어야 안전하다.
 */
const COMPRESSIBLE =
  /^(?:text\/(?:html|css|plain|xml)|application\/(?:json|javascript|xml|manifest\+json)|image\/svg\+xml)\b/i;

/** 이보다 작으면 압축해도 헤더값을 못 건진다. 크기를 아는 경우에만 적용된다. */
const MIN_BYTES = 1024;

/** `Vary` 를 **덮어쓰지 않고** 더한다. 이미 들어 있으면 그대로 둔다. */
function addVary(headers: Headers, field: string): void {
  const cur = headers.get('vary');
  if (!cur) { headers.set('vary', field); return; }
  const has = cur.split(',').some((v) => v.trim().toLowerCase() === field.toLowerCase());
  if (!has) headers.set('vary', `${cur}, ${field}`);
}

/**
 * 압축해도 되는 응답이면 gzip 으로 감싼 새 Response 를, 아니면 원본을 그대로 돌려준다.
 *
 * ★`CompressionStream` 으로 **파이프**한다(버퍼링 없음). `gzipSync` 로 짜면 5.5MB 응답을
 *   통째로 메모리에 올렸다가 압축하게 되고, 첫 바이트까지의 시간도 그만큼 늦어진다.
 * ★`content-length` 는 **반드시 지운다.** 압축 후 크기를 미리 모르는데 남겨두면 클라이언트가
 *   원본 길이만큼 기다리다 끊는다.
 */
export function maybeCompress(res: Response, request: Request): Response {
  // ★이미 압축된 것은 건드리지 않는다. Phase 3 방출물은 빌드 때 구운 `.gz` 를 그대로
  //   흘리며(`content-index/[collection].ts`) 요청당 CPU 가 0 이다 — 다시 압축하면
  //   그 이점을 버리고 **이중 인코딩**으로 응답이 깨진다. (그쪽은 Vary 를 스스로 붙인다.)
  if (res.headers.has('content-encoding')) return res;

  if (!res.body) return res;                              // 본문 없음(리다이렉트 등)
  if (res.status === 204 || res.status === 304) return res;

  if (!COMPRESSIBLE.test(res.headers.get('content-type') ?? '')) return res;

  // 크기를 아는 경우에만 하한을 적용한다. SSR HTML 은 스트림이라 length 가 없고,
  // 그건 대개 **큰 쪽**이므로 모르면 압축하는 편이 맞다.
  // (실측: 이 앱은 API 응답에도 content-length 를 대개 안 붙여서 이 하한은 거의 안 문다.
  //  379B 짜리 `/api/user-state` 도 178B 로 줄었으니 손해는 아니다.)
  const len = Number(res.headers.get('content-length'));
  const tooSmall = Number.isFinite(len) && len > 0 && len < MIN_BYTES;

  // ★여기까지 왔으면 이 URL 은 **Accept-Encoding 에 따라 다른 바이트를 낸다.** 그러니
  //   실제로 압축하든 안 하든 `Vary` 를 붙여야 한다. gzip 응답에만 붙이면 캐시가 비압축
  //   응답을 Accept-Encoding 과 무관하게 저장하게 되고, 같은 자원에 대해 Vary 가 응답마다
  //   달라진다 — 프록시·CDN 이 들어오는 Phase 5 에서 정확히 문제가 되는 형태다.
  const headers = new Headers(res.headers);
  addVary(headers, 'Accept-Encoding');

  const wantsGzip = /\bgzip\b/i.test(request.headers.get('accept-encoding') ?? '');
  if (!wantsGzip || tooSmall) {
    return new Response(res.body, { status: res.status, statusText: res.statusText, headers });
  }

  headers.set('content-encoding', 'gzip');
  headers.delete('content-length');

  return new Response(res.body.pipeThrough(new CompressionStream('gzip')), {
    status: res.status,
    statusText: res.statusText,
    headers,
  });
}
