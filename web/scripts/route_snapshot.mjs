#!/usr/bin/env node
// 라우트 응답 스냅샷 — Phase 3(SSR 제거 → SPA) 회귀 안전망.
//
// ★왜 필요한가: Phase 3 는 사용자 대면 25개 페이지를 클라이언트 렌더링으로 옮긴다.
//   로드맵이 "사장님이 매일 쓰는 웹을 고치는 작업 → 페이지 단위 점진 이전, 45개를 한 번에
//   뒤집지 않는다" 고 경고한 그 공사다. 눈으로 몇 개 열어보고 판단하면 나머지가 조용히 깨진다.
//   (같은 날 디코더 파서에서 안전망이 개악 430건을 잡았다 — 없었으면 그대로 나갔다.)
//
// ★인증: 페이지 대부분이 로그인 게이팅이라 무인증 스냅샷은 전부 302 라 쓸모가 없다. 두 방법이 있다.
//   ① `DEV_NOAUTH=1` — 미들웨어가 합성 admin 을 **주입**한다. 빠르지만 인증 경로를 건너뛰므로
//      **인증을 바꾸는 변경은 검증하지 못한다**(게이팅 이전·쿠키→토큰·CSRF→베어러가 전부 여기다).
//   ② `--cookie` — `snapshot_session.mjs --mint` 로 받은 진짜 세션 쿠키를 들고 간다. 실제
//      미들웨어가 실제로 해석하므로 인증 변경이 **정면으로** 검증된다. 인증을 건드릴 땐 ②를 쓴다.
//
// 사용:
//   node web/scripts/route_snapshot.mjs --base http://127.0.0.1:4399 --out /tmp/routes_before.json
//   T=$(node web/scripts/snapshot_session.mjs --mint)
//   node web/scripts/route_snapshot.mjs --base http://127.0.0.1:4324 --cookie "$T" --out /tmp/a.json
//   node web/scripts/route_snapshot.mjs --diff /tmp/routes_before.json /tmp/routes_after.json
//
// 저장하는 것(렌더 방식이 바뀌어도 의미가 남는 것만):
//   status · 본문 길이 · <title> · h1/h2 텍스트 · main 안의 링크 수 · 스크립트 태그 수
//   ★HTML 전문을 해시하지 않는다 — SPA 전환은 마크업을 통째로 바꾸므로 전부 '변경' 으로 떠서
//     신호가 죽는다. 사용자가 보는 것(제목·헤딩·링크 수)이 유지되는지를 본다.
import { readFileSync, writeFileSync } from 'node:fs';

const args = process.argv.slice(2);
const arg = (k, d = null) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };

// 동적 라우트는 대표 인스턴스로 찍는다(빌드된 실제 URL 이어야 의미가 있다).
const ROUTES = [
  '/', '/atlas', '/graph', '/paths', '/tools', '/log', '/progress',
  '/concepts/', '/problems/', '/problems/units', '/mistakes/', '/syntheses/',
  '/exam/', '/exam/random',
  '/account', '/settings', '/login', '/signup', '/privacy', '/terms',
  // 동적 — 대표 1건씩
  '/concepts/algebra/math-1/지수와_로그',
  '/problems/2026/수능/2026_수능_공통_01',
];

function extract(html) {
  const pick = (re) => { const m = html.match(re); return m ? m[1].replace(/\s+/g, ' ').trim().slice(0, 120) : null; };
  const all = (re) => (html.match(re) || []).length;
  return {
    title: pick(/<title[^>]*>([\s\S]*?)<\/title>/i),
    h1: pick(/<h1[^>]*>([\s\S]*?)<\/h1>/i),
    h2count: all(/<h2\b/gi),
    links: all(/<a\s[^>]*href=/gi),
    scripts: all(/<script\b/gi),
    forms: all(/<form\b/gi),
    len: html.length,
  };
}

async function snap(base, out, cookie) {
  const res = {};
  // 세션 쿠키 이름은 auth.ts 의 SESSION_COOKIE 와 같아야 한다. 값만 넘겨도 되고 `이름=값` 도 받는다.
  const headers = cookie
    ? { cookie: cookie.includes('=') ? cookie : `ms_session=${cookie}` }
    : undefined;
  for (const r of ROUTES) {
    const url = base.replace(/\/$/, '') + r;
    try {
      const t0 = Date.now();
      const resp = await fetch(url, { redirect: 'manual', headers });
      const html = resp.status === 200 ? await resp.text() : '';
      res[r] = { status: resp.status, ms: Date.now() - t0, ...(html ? extract(html) : {}) };
      const s = res[r];
      console.log(`  ${String(resp.status).padEnd(3)} ${r.padEnd(42)} ${s.len ?? '-'}B ${s.ms}ms ${s.title ?? ''}`);
    } catch (e) {
      res[r] = { status: 0, error: String(e).slice(0, 120) };
      console.log(`  ERR ${r} — ${res[r].error}`);
    }
  }
  writeFileSync(out, JSON.stringify(res, null, 1));
  const ok = Object.values(res).filter((v) => v.status === 200).length;
  const redir = Object.values(res).filter((v) => v.status === 302 || v.status === 301).length;
  const err = Object.values(res).filter((v) => v.status === 0).length;
  console.log(`\n✓ ${Object.keys(res).length}개 라우트 → ${out}  (200: ${ok} · 리다이렉트: ${redir} · 실패: ${err})`);

  // ★내용 없는 스냅샷이 조용히 저장되는 것을 막는다. 전부 302 면 "로그인 화면 22장", 전부 ERR 이면
  //   "빈 파일 22개" — 둘 다 자기들끼리는 똑같아서 **비교하면 늘 통과한다.** 안전망이 아니라 장식이 된다.
  //   (첫 시도에서 실제로 겪었다: 포트를 틀려 22개 전부 fetch failed 인데 exit 0 이었다.)
  if (ok === 0) {
    console.error(`\n🔴 200 이 하나도 없다 — 이 스냅샷은 비교 기준으로 쓸 수 없다.`);
    if (err) console.error(`   ${err}개가 연결 실패다. --base 를 확인한다(컨테이너 안이면 :8080, 호스트면 :4324).`);
    else if (redir) console.error(`   ${redir}개가 리다이렉트다. 쿠키가 안 먹었다 — 만료됐거나 이름이 auth.ts 의 SESSION_COOKIE 와 다르다.`);
    process.exitCode = 1;
  } else if (cookie && redir > ok) {
    console.error(`\n🔴 쿠키를 줬는데 리다이렉트(${redir})가 200(${ok})보다 많다 — 세션이 부분적으로만 먹었다.`);
    process.exitCode = 1;
  }
  return res;
}

function diff(aP, bP) {
  const a = JSON.parse(readFileSync(aP, 'utf8'));
  const b = JSON.parse(readFileSync(bP, 'utf8'));
  const keys = [...new Set([...Object.keys(a), ...Object.keys(b)])].sort();
  let bad = 0, changed = 0;
  for (const k of keys) {
    const x = a[k] ?? {}, y = b[k] ?? {};
    const notes = [];
    if (x.status !== y.status) notes.push(`status ${x.status}→${y.status}`);
    // 사용자가 보는 것이 사라졌는가 — SPA 전환이라도 이건 유지돼야 한다
    if (x.title && x.title !== y.title) notes.push(`title "${x.title}"→"${y.title}"`);
    if (x.h1 && x.h1 !== y.h1) notes.push(`h1 "${x.h1}"→"${y.h1}"`);
    if (x.h2count != null && y.h2count != null && x.h2count !== y.h2count) notes.push(`h2 ${x.h2count}→${y.h2count}`);
    if (x.links != null && y.links != null && Math.abs(x.links - y.links) > Math.max(3, x.links * 0.2))
      notes.push(`링크 ${x.links}→${y.links}`);
    if (!notes.length) continue;
    // status 회귀·콘텐츠 소실은 차단 신호
    const blocking = x.status === 200 && y.status !== 200
      || (x.h1 && !y.h1) || (x.title && !y.title);
    if (blocking) bad++;
    changed++;
    console.log(`${blocking ? '🔴' : '🟡'} ${k}\n     ${notes.join(' · ')}`);
  }
  console.log(`\n대상 ${keys.length} · 변경 ${changed} · 차단 ${bad}`);
  return bad ? 1 : 0;
}

const d = arg('--diff') ? [arg('--diff'), args[args.indexOf('--diff') + 2]] : null;
if (d) process.exit(diff(d[0], d[1]));
else await snap(arg('--base', 'http://127.0.0.1:4399'), arg('--out', '/tmp/routes.json'), arg('--cookie'));
