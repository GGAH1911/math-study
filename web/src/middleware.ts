// 전역 미들웨어 — 세션 해석 + 로그인 게이팅 + CSRF(동일출처) 검증.
// 보안 원칙: fail-safe. 세션 해석 실패는 throw 하지 않고 미인증으로 취급한다.
import { defineMiddleware } from 'astro:middleware';
import { resolveAuth, isSameOrigin, type User } from './lib/auth.ts';
import { rateLimit, sweep } from './lib/rate-limit.ts';
import { serveProblemImage } from './lib/webp-serve.ts';
import { corsOrigin, corsHeaders, preflight } from './lib/cors.ts';

// 남용방지: 비싼 POST 엔드포인트 per-user 분당 한도(429). 스팸/DoS 방지(빌링 아님).
const RATE_LIMITS: Array<[RegExp, number]> = [
  [/^\/api\/chat\b/, 25],        // LLM 튜터
  [/^\/api\/openrouter\b/, 25],  // 폴백 LLM
  [/^\/api\/sympy\b/, 60],       // 검증 계산(튜터가 다회 호출 가능)
];

// 로컬 검증 전용 우회(DEV_NOAUTH=1). 합성 admin 을 주입하고 인증·CSRF·admin 게이팅을
// 전부 통과시킨다 → admin 계정 없이도 검증자(Claude)가 모든 페이지 렌더를 직접 확인.
// ★real 서버(4323/4324)는 이 env 가 없어 절대 영향 없음. 반드시 127.0.0.1 바인드로만 띄울 것
// (네트워크 노출 시 무인증 admin 접근이 되므로 server.sh 가 noauth 면 MATH_STUDY_HOST=127.0.0.1 강제).
// ★dev 모드(astro dev)에서만 — 프로덕션 빌드(import.meta.env.DEV=false)에선 env 가 새도 절대 우회 불가.
const DEV_NOAUTH = import.meta.env.DEV && process.env.DEV_NOAUTH === '1';
const DEV_NOAUTH_USER: User = {
  id: '00000000-0000-0000-0000-000000000000',
  email: 'hwangi0404@gmail.com',
  display_name: 'DEV (noauth)',
  is_legacy: false,
  is_active: true,
  is_admin: true,
};

// 공개 라우트(미인증 허용).
const PUBLIC_PATHS: RegExp[] = [
  /^\/login\/?$/,
  /^\/signup\/?$/,
  /^\/terms\/?$/,    // 이용약관(가입 전 열람·법적 고지)
  /^\/privacy\/?$/,  // 개인정보처리방침(가입 전 열람·법적 고지)
  /^\/api\/auth\//, // 로그인/가입/로그아웃 API
  /^\/api\/health\b/,
  // ★프로덕션 게이팅(2026-06): dev 도구/진행관측 라우트는 더 이상 PUBLIC 아님.
  //   /dev/* 는 ADMIN_PATHS 로, /progress·/api/progress 는 로그인 필요로 강등(무인증 노출 차단).
  //   개발 중 비로그인 열람이 필요하면 DEV_NOAUTH(=dev 모드 전용)로 우회.
];

// 관리자 전용 경로(인증 + is_admin 필요). 비관리자: 페이지=홈, API=403.
const ADMIN_PATHS: RegExp[] = [
  /^\/dev(\/|$)/,              // 개발/디버그 도구 페이지(figure-test·rounds·variants 등)
  /^\/api\/regenerate-body\b/, // 공유 개념 본문 LLM 재생성(저작 행위)
  /^\/api\/figure-triage\b/,   // figure 트리아지 분류 저장(어드민)
  /^\/api\/dev(\/|$)/,          // dev 도구 API(3D 카메라 저장 등) — 저작 행위라 어드민만
  /^\/log\/?$/,               // LWIP 운영 로그(promote/prune/restructure/ingest…) — 개발 기록
];

// 정적/내부 자산·dev 모듈은 미들웨어 게이팅에서 제외(인증·CSRF 무관).
// dev(Vite) 경로(/@vite, /@fs, /@id, /src/, /node_modules/.vite)와 빌드 자산(/_astro)을
// 게이팅하면 모듈 로드·HMR 이 깨지므로 반드시 통과시킨다.
function isAssetOrInternal(pathname: string): boolean {
  // ★기출 원본 이미지는 자산이지만 인증 뒤로 게이팅(무인증 스크래핑 차단·유료화 전제).
  //   .png 확장자 regex(아래)로도 우회되지 않게 자산 판정보다 먼저 false 반환.
  if (pathname.startsWith('/problem-images/')) return false;
  if (
    pathname.startsWith('/@') ||
    pathname.startsWith('/_') ||
    pathname.startsWith('/src/') ||
    pathname.startsWith('/node_modules') ||
    pathname.startsWith('/assets/') ||
    pathname.startsWith('/favicon') ||
    pathname === '/sw.js' ||
    pathname === '/manifest.webmanifest'
  ) return true;
  return /\.(css|m?js|cjs|ts|tsx|jsx|map|json|png|jpe?g|svg|webp|gif|avif|ico|woff2?|ttf|eot|txt|wasm)$/i.test(pathname);
}

export const onRequest = defineMiddleware(async (context, next) => {
  const { request, cookies, url } = context;
  const pathname = url.pathname;

  if (isAssetOrInternal(pathname)) return next();

  // 로컬 검증 전용 포트: 합성 admin 주입 후 모든 게이팅 우회(real 서버는 DEV_NOAUTH 미설정).
  if (DEV_NOAUTH) {
    context.locals.user = DEV_NOAUTH_USER;
    return next();
  }

  const method = request.method.toUpperCase();

  // 교차출처 preflight 는 자격증명이 실리기 **전에** 온다 — 인증·게이팅보다 앞서 답해야 한다.
  const xOrigin = corsOrigin(request);
  if (method === 'OPTIONS' && xOrigin) return preflight(xOrigin);

  // 세션 → 유저 해석(fail-safe). ★CSRF 검사보다 **먼저** 한다: 베어러로 인증됐는지 알아야
  //   동일출처 검사를 건너뛸지 판단할 수 있기 때문이다(아래).
  let user = null;
  let via: 'bearer' | 'cookie' | null = null;
  try { ({ user, via } = await resolveAuth(request, cookies)); } catch { user = null; via = null; }
  context.locals.user = user;

  // CSRF: state-changing 요청은 동일출처만 허용(SameSite=Lax 쿠키 + Origin 검증 이중방어).
  //
  // ★베어러로 인증된 요청은 면제한다. CSRF 가 성립하는 이유는 브라우저가 쿠키를 **자동으로**
  //   실어 보내기 때문이다. 베어러는 코드가 명시적으로 붙여야 하므로 남의 페이지가 시킬 수 없고,
  //   토큰을 이미 가진 공격자에겐 CSRF 가 무의미하다. 그래서 앱(교차출처)이 통과할 수 있다.
  // ★조건이 `via === 'bearer'` 인 것이 중요하다. "Authorization 헤더가 있으면" 으로 짜면
  //   쿠키로 로그인한 브라우저에 아무 헤더나 붙여 검사를 무력화할 수 있다. resolveAuth 는
  //   베어러가 틀리면 쿠키로 떨어지며 via 를 'cookie' 로 돌려주므로 그 구멍이 막힌다.
  if (method === 'POST' || method === 'PUT' || method === 'PATCH' || method === 'DELETE') {
    if (via !== 'bearer' && !isSameOrigin(request)) {
      return new Response('cross-origin request rejected', { status: 403 });
    }
  }

  const isPublic = PUBLIC_PATHS.some((re) => re.test(pathname));
  if (isPublic) {
    // 이미 로그인했는데 로그인/가입 페이지로 가면 홈으로.
    if (user && (pathname.startsWith('/login') || pathname.startsWith('/signup'))) {
      return context.redirect('/');
    }
    return next();
  }

  // 보호 경로 미인증: API는 401 JSON, 페이지는 /login?returnTo= 로 리다이렉트.
  if (!user) {
    if (pathname.startsWith('/api/')) {
      return new Response(JSON.stringify({ error: 'unauthorized' }), {
        status: 401,
        headers: { 'content-type': 'application/json' },
      });
    }
    const returnTo = encodeURIComponent(pathname + url.search);
    return context.redirect(`/login?returnTo=${returnTo}`);
  }

  // 기출 이미지: **인증을 통과한 요청만 여기까지 온다.** WebP 우선, 안 되면 원본
  // (실측 무손실 39.6%). 경로는 `.png` 그대로 — 개명은 Phase 5.
  //
  // ★2026-08-14 에 이 블록이 **실제로 동작하기 시작했다.** 그 전까지는 `public/` 안에 있는
  //   파일을 정적 핸들러가 미들웨어보다 먼저 응답해 **무인증 200** 이었고(기출 5,774장이
  //   로그인 없이 열림), 같은 이유로 위 54-56 줄의 "무인증 스크래핑 차단" 도 죽어 있었다.
  //   파일을 `web/private/` 로 옮겨 정적 서빙에서 떼어내니 둘 다 살아났다(`media-root.ts`).
  //   ⚠️ 이미지를 다시 `web/public/` 로 되돌리면 **게이팅이 조용히 꺼진다.** 티가 안 난다.
  if (method === 'GET' && pathname.startsWith('/problem-images/')) {
    const res = await serveProblemImage(pathname, request);
    // 못 찾으면 없는 파일이다. next() 로 흘리면 SSR 라우터가 받아 엉뚱한 응답을 준다.
    return res ?? new Response('not found', { status: 404 });
  }

  // 남용방지: 인증된 사용자라도 비싼 엔드포인트는 분당 한도 초과 시 429.
  if (method === 'POST') {
    for (const [re, limit] of RATE_LIMITS) {
      if (re.test(pathname)) {
        sweep(60_000);
        if (!rateLimit(`${user.id}:${pathname}`, limit, 60_000)) {
          return new Response(JSON.stringify({ error: '요청이 너무 잦습니다. 잠시 후 다시 시도해 주세요.' }), {
            status: 429,
            headers: { 'content-type': 'application/json' },
          });
        }
        break;
      }
    }
  }

  // 관리자 전용 경로 — dev 도구 + 공유 콘텐츠(개념 본문) 재생성.
  // 인증은 됐지만 admin 이 아닌 사용자는 차단: 페이지=홈, API=403.
  if (ADMIN_PATHS.some((re) => re.test(pathname)) && !user.is_admin) {
    if (pathname.startsWith('/api/')) {
      return new Response(JSON.stringify({ error: 'forbidden: admin only' }), {
        status: 403,
        headers: { 'content-type': 'application/json' },
      });
    }
    return context.redirect('/');
  }

  // 허용 출처(앱)의 응답에만 CORS 헤더를 얹는다. 동일출처(웹)는 xOrigin 이 null 이라 그대로 나간다 —
  // 즉 이 블록은 웹 응답을 한 바이트도 바꾸지 않는다.
  if (xOrigin) {
    const res = await next();
    const headers = new Headers(res.headers);
    for (const [k, v] of Object.entries(corsHeaders(xOrigin))) headers.set(k, v);
    return new Response(res.body, { status: res.status, statusText: res.statusText, headers });
  }

  return next();
});
