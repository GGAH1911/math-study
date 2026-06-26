// 전역 미들웨어 — 세션 해석 + 로그인 게이팅 + CSRF(동일출처) 검증.
// 보안 원칙: fail-safe. 세션 해석 실패는 throw 하지 않고 미인증으로 취급한다.
import { defineMiddleware } from 'astro:middleware';
import { resolveUser, isSameOrigin, type User } from './lib/auth.ts';
import { rateLimit, sweep } from './lib/rate-limit.ts';

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

  // CSRF: state-changing 요청은 동일출처만 허용(SameSite=Lax 쿠키 + Origin 검증 이중방어).
  const method = request.method.toUpperCase();
  if (method === 'POST' || method === 'PUT' || method === 'PATCH' || method === 'DELETE') {
    if (!isSameOrigin(request)) {
      return new Response('cross-origin request rejected', { status: 403 });
    }
  }

  // 세션 → 유저 해석(fail-safe).
  let user = null;
  try { user = await resolveUser(cookies); } catch { user = null; }
  context.locals.user = user;

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

  return next();
});
