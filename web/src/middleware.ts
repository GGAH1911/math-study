// 전역 미들웨어 — 세션 해석 + 로그인 게이팅 + CSRF(동일출처) 검증.
// 보안 원칙: fail-safe. 세션 해석 실패는 throw 하지 않고 미인증으로 취급한다.
import { defineMiddleware } from 'astro:middleware';
import { resolveUser, isSameOrigin, type User } from './lib/auth.ts';

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
  /^\/api\/auth\//, // 로그인/가입/로그아웃 API
  /^\/api\/health\b/,
  /^\/progress\/?$/,    // 인제스트 진행 관측 — 개발용, 미인증 허용
  /^\/api\/progress\b/, // progress 폴링 API
  /^\/dev\/concept-figure-test\/?$/, // figure 디자인 검증 — 정적 데모(데이터 없음), 비로그인 허용
  /^\/dev\/concept-figures\/?$/,     // 개념 도식 갤러리 검토 — 비민감 도식, 비로그인 허용(임시)
  /^\/dev\/figrender\/?$/,           // QA 단일 도식 렌더 하네스(고정폭) — 헤드리스 스샷용
  /^\/dev\/ingest-test\/?$/,         // 기출 인제스트 agy 교정+도식 테스트(임시) — 비로그인 열람
  /^\/dev\/figextract\/?$/,          // 그림 추출 프로토타입 뷰어(임시) — 비로그인 열람
  /^\/dev\/corrector-gallery\/?$/,   // 교정기 결과 갤러리(임시) — 비로그인 열람
];

// 관리자 전용 경로(인증 + is_admin 필요). 비관리자: 페이지=홈, API=403.
const ADMIN_PATHS: RegExp[] = [
  /^\/dev(\/|$)/,              // 개발/디버그 도구 페이지(figure-test·rounds·variants 등)
  /^\/api\/regenerate-body\b/, // 공유 개념 본문 LLM 재생성(저작 행위)
  /^\/log\/?$/,               // LWIP 운영 로그(promote/prune/restructure/ingest…) — 개발 기록
];

// 정적/내부 자산·dev 모듈은 미들웨어 게이팅에서 제외(인증·CSRF 무관).
// dev(Vite) 경로(/@vite, /@fs, /@id, /src/, /node_modules/.vite)와 빌드 자산(/_astro)을
// 게이팅하면 모듈 로드·HMR 이 깨지므로 반드시 통과시킨다.
function isAssetOrInternal(pathname: string): boolean {
  if (
    pathname.startsWith('/@') ||
    pathname.startsWith('/_') ||
    pathname.startsWith('/src/') ||
    pathname.startsWith('/node_modules') ||
    pathname.startsWith('/assets/') ||
    pathname.startsWith('/problem-images/') ||
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
