// 파생 상태(problem_state·concept_mastery)를 정본에서 다시 만들어 **대조**하고, 원하면 적용한다.
//
// ★기본은 dry-run. `--apply` 를 줘야 쓴다.
// ★적용은 **이벤트 로그로 이력이 온전히 덮이는 대상에만** 한다. 로그 개시(2026-08-13) 이전
//   이력을 가진 행을 덮어쓰면 그 시절의 mark-mastered·숙련도가 조용히 사라진다.
//   억지로 하려면 `--include-legacy` 를 명시해야 한다(그 뜻을 알고 쓰라는 뜻이다).
//
// 실행: docker compose -f deploy/docker-compose.yml exec -T web \
//         node --experimental-strip-types --import ./scripts/ts-resolve-hook.mjs \
//              scripts/recompute_derived.mjs [--apply] [--include-legacy]
import sql from '../src/lib/db.ts';
import { replayProblemStates, replayConceptMastery, isCovered, key } from '../src/lib/recompute.ts';

const APPLY = process.argv.includes('--apply');
const LEGACY = process.argv.includes('--include-legacy');

const [attempts, events, actualStates, actualMastery, [{ started }]] = await Promise.all([
  sql`SELECT user_id, problem_id, is_correct, attempted_at FROM problem_attempts`,
  sql`SELECT user_id, kind, target, payload, occurred_at, seq FROM learning_events`,
  sql`SELECT user_id, problem_id, status, review_state,
             to_char(next_review,'YYYY-MM-DD') AS next_review, attempt_count FROM problem_state`,
  sql`SELECT user_id, concept_id, mastery, mastery_evidence FROM concept_mastery`,
  sql`SELECT min(recorded_at) AS started FROM learning_events`,
]);
const logStart = started ? +new Date(started) : Infinity;

// 대상별 최초 접촉 시각 — 로그 개시 이전이면 재계산이 그 이력을 알 수 없다.
const firstTouch = new Map();
const note = (k, t) => { const p = firstTouch.get(k); if (p === undefined || t < p) firstTouch.set(k, t); };
for (const a of attempts) note(key(a.user_id, a.problem_id), +new Date(a.attempted_at));
for (const e of events) {
  const id = e.kind.startsWith('problem.') ? e.payload?.problemId : e.target;
  if (id) note(key(e.user_id, id), +new Date(e.occurred_at));
}

const states = replayProblemStates(attempts, events);
const mastery = replayConceptMastery(events);

const fmt = (v) => (v == null ? null : v instanceof Date ? v.toISOString().slice(0, 10) : String(v).slice(0, 10));
const sameState = (a, b) => a && b && a.status === b.status && a.review_state === b.review_state
  && fmt(a.next_review) === fmt(b.next_review) && a.attempt_count === b.attempt_count;

let ok = 0; const toWrite = [], toDelete = [], legacySkipped = [], mismatch = [];
const seen = new Set();
for (const a of actualStates) {
  const k = key(a.user_id, a.problem_id); seen.add(k);
  const r = states.get(k);
  if (sameState(r, a)) { ok++; continue; }
  const covered = isCovered(firstTouch.get(k), logStart);
  if (!covered && !LEGACY) { legacySkipped.push(k); continue; }
  mismatch.push(k);
  if (r) toWrite.push({ user_id: a.user_id, problem_id: a.problem_id, ...r });
  else toDelete.push({ user_id: a.user_id, problem_id: a.problem_id });
}
// 실제엔 없는데 재생에는 있는 것 — 파생 상태가 유실된 경우(복원 대상).
for (const [k, r] of states) {
  if (seen.has(k)) continue;
  const [user_id, problem_id] = k.split('|');
  if (!isCovered(firstTouch.get(k), logStart) && !LEGACY) { legacySkipped.push(k); continue; }
  mismatch.push(k); toWrite.push({ user_id, problem_id, ...r });
}

console.log(`problem_state  실제 ${actualStates.length}행 · 재생 ${states.size}행`);
console.log(`  일치 ${ok} · 차이 ${mismatch.length} · 로그이전이라 건너뜀 ${legacySkipped.length}`);
console.log(`  적용하면: 갱신/생성 ${toWrite.length} · 삭제 ${toDelete.length}`);

let mOk = 0; const mWrite = [];
for (const [k, r] of mastery) {
  const [user_id, concept_id] = k.split('|');
  const cur = actualMastery.find((m) => m.user_id === user_id && m.concept_id === concept_id);
  if (cur && cur.mastery === r.mastery
      && JSON.stringify(cur.mastery_evidence) === JSON.stringify(r.mastery_evidence)) { mOk++; continue; }
  mWrite.push({ user_id, concept_id, ...r });
}
console.log(`concept_mastery 이벤트 유래 ${mastery.size}건 · 일치 ${mOk} · 차이 ${mWrite.length}`);

if (!APPLY) { console.log('\n[dry-run] --apply 를 줘야 씁니다.'); await sql.end(); process.exit(0); }

await sql.begin(async (tx) => {
  for (const d of toDelete) {
    await tx`DELETE FROM problem_state WHERE user_id = ${d.user_id} AND problem_id = ${d.problem_id}`;
  }
  for (const w of toWrite) {
    await tx`
      INSERT INTO problem_state (user_id, problem_id, status, review_state, next_review, last_attempted, attempt_count)
      VALUES (${w.user_id}, ${w.problem_id}, ${w.status}, ${w.review_state}, ${w.next_review}, NOW(), ${w.attempt_count})
      ON CONFLICT (user_id, problem_id) DO UPDATE SET
        status = EXCLUDED.status, review_state = EXCLUDED.review_state,
        next_review = EXCLUDED.next_review, attempt_count = EXCLUDED.attempt_count`;
  }
  for (const m of mWrite) {
    await tx`
      INSERT INTO concept_mastery (user_id, concept_id, mastery, mastery_evidence, mastery_updated)
      VALUES (${m.user_id}, ${m.concept_id}, ${m.mastery}, ${sql.json(m.mastery_evidence)}, NOW())
      ON CONFLICT (user_id, concept_id) DO UPDATE SET
        mastery = EXCLUDED.mastery, mastery_evidence = EXCLUDED.mastery_evidence, mastery_updated = NOW()`;
  }
});
console.log(`\n[적용] problem_state 쓰기 ${toWrite.length} · 삭제 ${toDelete.length} · concept_mastery 쓰기 ${mWrite.length}`);
await sql.end();
