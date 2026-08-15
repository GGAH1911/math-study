#!/usr/bin/env node
// 스냅샷용 세션 발급/회수 — 인증 회귀 안전망의 빠진 조각.
//
// ★왜 필요한가: `route_snapshot.mjs` 는 지금까지 `DEV_NOAUTH=1` 로 인증을 **우회**해 찍었다.
//   그래서 "인증을 바꾸는 변경"만 검증할 수 없었다 — 위험이 가장 큰 자리가 안전망의 사각지대였다.
//   Phase 3 의 게이팅 이전·쿠키→토큰·CSRF→베어러가 전부 그 자리에 있다.
//
// ★어떻게: 세션은 DB 행이다(`sessions.token_hash` = sha256(token), `web/src/lib/auth.ts` 참조).
//   그래서 행을 심어 진짜 쿠키를 만든다. 실제 미들웨어가 그 쿠키를 실제로 해석하므로
//   게이팅·CSRF·admin 판정이 전부 진짜 경로로 실행된다. 우회가 아니라 **정면으로 통과시키는** 것이다.
//
// ★왜 전용 계정인가: 사장님 계정으로 찍으면 조회만으로도 학습 이벤트가 남을 수 있고, 스냅샷이
//   사장님 데이터 변화에 흔들려 회귀 신호가 죽는다. 전용 계정은 비어 있어 **결정적**이다.
//   데이터가 많은 화면까지 보려면 `--email` 로 다른 계정을 지정한다.
//
// ★이 계정으로는 **로그인할 수 없다**: password_hash 와 oauth_* 를 비운 채 만든다. 들어오는
//   길은 여기서 심는 세션 하나뿐이고, 그 세션은 1시간이면 죽는다.
//
// 사용:
//   node web/scripts/snapshot_session.mjs --mint            # 토큰 출력(쿠키 값)
//   node web/scripts/snapshot_session.mjs --revoke <token>
//   node web/scripts/snapshot_session.mjs --revoke-all      # 이 계정의 세션 전부
import { createHash, randomBytes } from 'node:crypto';
import postgres from 'postgres';

const args = process.argv.slice(2);
const arg = (k, d = null) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const has = (k) => args.includes(k);

const EMAIL = arg('--email', 'snapshot+harness@math-study.local');
// 30일(실사용 세션)이 아니라 1시간. 유출돼도 곧 죽고, 스냅샷은 몇 분이면 끝난다.
const TTL_MS = 60 * 60 * 1000;

const DB = process.env.MATH_STUDY_DATABASE_URL;
if (!DB) { console.error('MATH_STUDY_DATABASE_URL 이 없다'); process.exit(2); }
const sql = postgres(DB, { max: 1 });
const hash = (t) => createHash('sha256').update(t).digest('hex');

try {
  if (has('--revoke')) {
    const r = await sql`DELETE FROM sessions WHERE token_hash = ${hash(arg('--revoke'))}`;
    console.log(`회수 ${r.count}건`);
  } else if (has('--revoke-all')) {
    const r = await sql`
      DELETE FROM sessions WHERE user_id IN (SELECT id FROM users WHERE lower(email) = lower(${EMAIL}))`;
    console.log(`회수 ${r.count}건 (${EMAIL})`);
  } else if (has('--mint')) {
    const [u] = await sql`
      INSERT INTO users (email, display_name, is_active)
      VALUES (${EMAIL}, ${'스냅샷 하네스'}, TRUE)
      ON CONFLICT (lower(email)) DO UPDATE SET updated_at = NOW()
      RETURNING id`;
    const token = randomBytes(32).toString('base64url');
    await sql`
      INSERT INTO sessions (user_id, token_hash, expires_at, user_agent, ip)
      VALUES (${u.id}, ${hash(token)}, ${new Date(Date.now() + TTL_MS)}, ${'route_snapshot'}, ${null})`;
    console.log(token);
  } else {
    console.error('--mint | --revoke <token> | --revoke-all  [--email <e>]');
    process.exit(2);
  }
} finally {
  await sql.end({ timeout: 5 });
}
