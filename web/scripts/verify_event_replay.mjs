// **이벤트만으로 파생 상태를 되살릴 수 있는가** 를 실제 데이터로 확인한다(읽기 전용).
//
// ★이게 Phase 4 선행 항목의 통과 조건이다. `reset`·`mark-mastered`·`skip` 을 이벤트로
//   남기지 않은 채 problem_attempts 로 재계산하면 **지운 상태가 되살아나고 사용자가 선언한
//   숙련·미룸이 사라진다.** 그래서 "이벤트가 있으면 복원된다" 를 말이 아니라 대조로 증명한다.
//
// 재생 입력 = problem_attempts(시도) + learning_events(사용자 의도). 둘을 시간순으로 합쳐
// 현재 problem_state 와 비교한다.
//
// 실행: docker compose -f deploy/docker-compose.yml exec -T web \
//         node --experimental-strip-types --import ./scripts/ts-resolve-hook.mjs scripts/verify_event_replay.mjs
import sql from '../src/lib/db.ts';
import { nextSrsState } from '../src/lib/srs.ts';

const events = await sql`
  SELECT user_id, kind, payload->>'problemId' AS problem_id, payload, occurred_at, seq
    FROM learning_events WHERE kind LIKE 'problem.%' ORDER BY occurred_at, seq`;
const attempts = await sql`
  SELECT user_id, problem_id, is_correct, attempted_at FROM problem_attempts ORDER BY attempted_at`;
const actual = await sql`
  SELECT user_id, problem_id, status, review_state,
         to_char(next_review, 'YYYY-MM-DD') AS next_review, attempt_count FROM problem_state`;
// ★로그 개시 시각. 이보다 앞선 이력은 재생 대상이 아니다 — 그때는 이벤트를 남기지 않았다.
//   이걸 구분하지 않으면 "복원 실패" 로 뭉뚱그려져 진짜 결함이 묻힌다.
const [{ started }] = await sql`SELECT min(recorded_at) AS started FROM learning_events`;
const legacyBefore = started ? +new Date(started) : Infinity;
const firstTouch = new Map();
for (const a of attempts) {
  const k = `${a.user_id}|${a.problem_id}`;
  if (!firstTouch.has(k)) firstTouch.set(k, +new Date(a.attempted_at));
}

// 시도와 이벤트를 하나의 시간축으로 — 오프라인 기기가 늦게 합류해도 순서는 occurred_at 이 정한다.
const timeline = [
  ...attempts.map((a) => ({ t: +new Date(a.attempted_at), kind: 'attempt', ...a })),
  ...events.map((e) => ({ t: +new Date(e.occurred_at), ...e })),
].sort((x, y) => x.t - y.t || (Number(x.seq ?? 0) - Number(y.seq ?? 0)));

const key = (r) => `${r.user_id}|${r.problem_id}`;
const replayed = new Map();
for (const ev of timeline) {
  if (!ev.problem_id) continue;
  const k = key(ev);
  if (ev.kind === 'problem.reset') { replayed.delete(k); continue; }
  const cur = replayed.get(k) ?? { status: 'unsolved', review_state: 'new', next_review: null, attempt_count: 0 };
  if (ev.kind === 'problem.mark_mastered') {
    replayed.set(k, { ...cur, status: 'solved', review_state: 'mature', next_review: ev.payload.nextReview, attempt_count: Math.max(1, cur.attempt_count) });
  } else if (ev.kind === 'problem.skip') {
    // skip 은 next_review 만 민다(신규면 행을 만든다) — API 의 ON CONFLICT 와 같은 규칙.
    replayed.set(k, replayed.has(k) ? { ...cur, next_review: ev.payload.nextReview }
                                    : { status: 'review', review_state: 'new', next_review: ev.payload.nextReview, attempt_count: 0 });
  } else if (ev.kind === 'attempt') {
    // ★재생은 **그 시도가 있었던 시각** 기준 — 그래서 nextSrsState 에 at 을 넘긴다.
    const tr = nextSrsState({ review_state: cur.review_state, attempt_count: cur.attempt_count }, ev.is_correct === true, new Date(ev.attempted_at));
    replayed.set(k, { status: tr.status, review_state: tr.reviewState, next_review: tr.nextReview, attempt_count: cur.attempt_count + 1 });
  }
}

let same = 0; const diffs = [];
const seen = new Set();
for (const a of actual) {
  const k = key(a); seen.add(k);
  const r = replayed.get(k);
  const norm = (v) => (v == null ? null : (v instanceof Date ? v.toISOString().slice(0, 10) : String(v).slice(0, 10)));
  if (r && r.status === a.status && r.review_state === a.review_state
      && norm(r.next_review) === norm(a.next_review) && r.attempt_count === a.attempt_count) same++;
  else diffs.push({ k, legacy: (firstTouch.get(k) ?? Infinity) < legacyBefore, actual: { s: a.status, r: a.review_state, n: norm(a.next_review), c: a.attempt_count },
                       replay: r ? { s: r.status, r: r.review_state, n: norm(r.next_review), c: r.attempt_count } : '(없음)' });
}
const extra = [...replayed.keys()].filter((k) => !seen.has(k));
const legacy = diffs.filter((d) => d.legacy);
const real = diffs.filter((d) => !d.legacy);

console.log(`실제 problem_state ${actual.length}행 · 재생 ${replayed.size}행`);
console.log(`  완전 일치              ${same}`);
console.log(`  불일치(로그 개시 이전) ${legacy.length}  ← 이벤트가 없던 시절의 이력. 복원 대상 아님`);
console.log(`  불일치(진짜)           ${real.length}`);
console.log(`  재생에만 있음          ${extra.length}`);
for (const d of real.slice(0, 8)) console.log('   ', JSON.stringify(d));
// ★reset 이 이벤트로 남았는지가 이 검증의 핵심: 남지 않았다면 '재생에만 있음' 으로 튄다
//   (시도 기록은 그대로라 상태가 되살아나므로).
console.log(`\n판정: ${real.length === 0 && extra.length === 0 ? '✅ 로그 개시 이후 이력은 이벤트+시도로 그대로 복원된다' : '❌ 복원 안 되는 항목이 있다'}`);
await sql.end();
