// 교차출처 허용 목록 — Capacitor 앱이 베어러 토큰으로 API 를 부르기 위한 최소 장치.
//
// ★왜 필요한가: 네이티브 앱의 WebView 는 `capacitor://localhost`(iOS) / `http://localhost`(Android)
//   출처에서 돈다. 우리 서버 입장에선 **교차출처**라, CORS 응답 헤더가 없으면 WebView 가 응답을
//   읽지 못한다. 로드맵 Phase 3 의 "베어러 토큰 + CORS 화이트리스트" 가 이것이다.
//
// ★★안전 설계의 핵심: **`Access-Control-Allow-Credentials` 를 절대 보내지 않는다.**
//   그 헤더가 없으면 브라우저는 교차출처 요청에 쿠키를 붙이지 않는다. 즉 교차출처에서 쓸 수 있는
//   자격증명은 **베어러뿐**이고, 베어러는 코드가 명시적으로 붙여야 하므로 남의 페이지가 시킬 수
//   없다. 결과적으로 CORS 를 열어도 CSRF 표면이 늘지 않는다 — 이게 쿠키 대신 토큰으로 가는 이유다.
//
// ★와일드카드(`*`)를 쓰지 않는다. 요청 Origin 이 목록에 **정확히** 있을 때만 그 값을 되돌려준다.
//   목록에 없으면 헤더를 아예 붙이지 않는다(= 브라우저가 막는다).

/** 기본값은 Capacitor 의 두 출처. 배포마다 다르면 `MS_CORS_ORIGINS` 로 덮는다(쉼표 구분). */
const DEFAULT_ORIGINS = ['capacitor://localhost', 'http://localhost', 'https://localhost'];

function allowed(): Set<string> {
  const env = process.env.MS_CORS_ORIGINS;
  const list = env ? env.split(',').map((s) => s.trim()).filter(Boolean) : DEFAULT_ORIGINS;
  return new Set(list);
}

/** 이 Origin 을 교차출처로 허용하는가. Origin 헤더가 없으면(동일출처·서버간) 대상이 아니다. */
export function corsOrigin(request: Request): string | null {
  const origin = request.headers.get('origin');
  if (!origin) return null;
  return allowed().has(origin) ? origin : null;
}

/** 허용된 Origin 에 붙일 응답 헤더. Allow-Credentials 는 **의도적으로 없다**(위 설명 참조). */
export function corsHeaders(origin: string): Record<string, string> {
  return {
    'access-control-allow-origin': origin,
    'access-control-allow-methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS',
    'access-control-allow-headers': 'authorization, content-type',
    'access-control-max-age': '600',
    // 같은 URL 이 Origin 에 따라 다른 응답을 주므로 캐시가 섞이지 않게 한다.
    vary: 'Origin',
  };
}

/** preflight(OPTIONS) 응답. 본문 없이 204. */
export function preflight(origin: string): Response {
  return new Response(null, { status: 204, headers: corsHeaders(origin) });
}
