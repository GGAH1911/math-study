#!/usr/bin/env node
// API 인증 게이팅 전수 검사 — Phase 3 에서 만든 엔드포인트가 **전부 인증 뒤**인지 확인한다.
//
// ★왜 필요한가: 페이지를 클라이언트로 옮기면 데이터가 **새 엔드포인트**로 나간다. 그런데
//   미들웨어의 게이팅 목록(`PUBLIC_PATHS`·`ADMIN_PATHS`)은 **페이지 경로 기준**이라
//   새 API 가 자동으로 보호되지 않는다. 실제로 `/log` 는 `ADMIN_PATHS` 에 있지만
//   `/api/log` 는 없어서 **API 에서 직접 막아야** 했다.
//   2026-08-14 에 기출 이미지 5,774장이 같은 계열(게이팅이 닿지 않는 경로)로 열려 있었다.
//
// ★"200 이 나온다"만 보면 안 된다. **무인증이 401 인지**가 핵심이고, 그게 이 스크립트의 존재 이유다.
//
// 사용:
//   node web/scripts/verify_api_gating.mjs --base http://127.0.0.1:8080 --cookie <token>
import { argv, exit } from 'node:process';

const arg = (k, d = null) => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : d; };
const BASE = (arg('--base', 'http://127.0.0.1:8080')).replace(/\/$/, '');
const COOKIE = arg('--cookie');

const enc = (s) => s.split('/').map(encodeURIComponent).join('/');

/** `admin: true` = 인증돼도 비어드민에겐 403 이어야 한다. */
const ENDPOINTS = [
  { path: `/api/content/concepts/${enc('algebra/math-1/지수와_로그')}` },
  { path: '/api/content-index/problems' },
  { path: `/api/exam/round/${enc('2026/수능')}` },
  { path: '/api/exam/random' },
  { path: '/api/concepts-overview' },
  { path: `/api/problems/${enc('2026/수능/2026_수능_공통_01')}` },
  { path: `/api/concepts/${enc('algebra/math-1/지수와_로그')}` },
  { path: '/api/user-state' },
  { path: '/api/learning-path' },
  { path: '/api/concept-graph' },
  { path: '/api/home' },
  { path: '/api/atlas' },
  { path: '/api/account' },
  { path: '/api/log', admin: true },
];

const code = async (path, cookie) => {
  try {
    const r = await fetch(BASE + path, {
      redirect: 'manual',
      headers: cookie ? { cookie: `ms_session=${cookie}` } : {},
    });
    return r.status;
  } catch (e) { return `ERR ${String(e).slice(0, 40)}`; }
};

if (!COOKIE) {
  console.error('--cookie 가 필요하다: node web/scripts/snapshot_session.mjs --mint');
  exit(2);
}

let bad = 0;
console.log(`  ${'엔드포인트'.padEnd(44)} 무인증  인증`);
for (const e of ENDPOINTS) {
  const anon = await code(e.path, null);
  const auth = await code(e.path, COOKIE);
  const wantAuth = e.admin ? 403 : 200;
  const ok = anon === 401 && auth === wantAuth;
  if (!ok) bad++;
  console.log(`  ${ok ? '✅' : '🔴'} ${e.path.slice(0, 42).padEnd(42)} ${String(anon).padEnd(7)} ${auth}${e.admin ? ' (어드민전용)' : ''}`);
  if (!ok) console.log(`       기대: 무인증 401 · 인증 ${wantAuth}`);
}

console.log(`\n${bad ? `🔴 게이팅 위반 ${bad}건` : `✅ ${ENDPOINTS.length}개 엔드포인트 — 전부 인증 뒤`}`);
// ★새 엔드포인트를 만들면 **이 목록에 추가해야 한다.** 빠뜨리면 이 게이트가 그것을 안 본다.
exit(bad ? 1 : 0);
