// 파생 상태(problem_state·concept_mastery)를 **정본으로부터 다시 만든다.**
//
// 정본 = `problem_attempts`(무슨 일이 있었나) + `learning_events`(사용자가 무엇을 의도했나).
// 둘 다 append-only 라, 파생 상태는 언제든 버리고 다시 계산할 수 있어야 한다 — 그게 오프라인
// 두 기기의 작업을 합칠 수 있는 유일한 방법이다(상태를 합치면 어느 쪽이 이겨야 할지 알 수 없다).
//
// ★재생 순서는 `occurred_at`(기기에서 일어난 시각)이다. 서버 도착순(`seq`)이 아니다 —
//   오프라인 기기가 3일 뒤 합류하면 그 사이 이벤트보다 **앞에** 끼어들어야 맞다.
//   `seq` 는 동기화 커서 전용이고, 여기서는 같은 시각일 때의 tiebreak 로만 쓴다.
//
// ⚠️ **로그 개시 이전 이력은 재생할 수 없다.** 그때는 이벤트를 남기지 않았다. 그래서
//    `coveredSince` 보다 앞선 이력을 가진 대상은 계산은 하되 **적용 대상에서 뺀다**
//    (덮어쓰면 그 시절의 mark-mastered·숙련도가 조용히 사라진다).
import { nextSrsState } from './srs.ts';

export interface AttemptRow { user_id: string; problem_id: string; is_correct: boolean | null; attempted_at: string | Date; }
export interface EventRow {
  user_id: string; kind: string; target: string;
  payload: Record<string, unknown>; occurred_at: string | Date; seq: string | number;
}
export interface DerivedState { status: string; review_state: string; next_review: string | null; attempt_count: number; }
export interface DerivedMastery { mastery: string; mastery_evidence: string[]; }

const ms = (v: string | Date) => +new Date(v);
export const key = (userId: string, targetId: string) => `${userId}|${targetId}`;

/** 시도와 이벤트를 하나의 시간축으로. 같은 시각이면 seq(서버 도착순)로 가른다. */
function timeline(attempts: AttemptRow[], events: EventRow[]) {
  return [
    ...attempts.map((a) => ({ t: ms(a.attempted_at), seq: 0, kind: 'attempt' as const, row: a })),
    ...events.map((e) => ({ t: ms(e.occurred_at), seq: Number(e.seq ?? 0), kind: e.kind, row: e })),
  ].sort((x, y) => x.t - y.t || x.seq - y.seq);
}

/** problem_state 재계산. 반환 키는 `${user_id}|${problem_id}`. */
export function replayProblemStates(attempts: AttemptRow[], events: EventRow[]): Map<string, DerivedState> {
  const out = new Map<string, DerivedState>();
  for (const ev of timeline(attempts, events.filter((e) => e.kind.startsWith('problem.')))) {
    const row = ev.row as AttemptRow & EventRow;
    const pid = ev.kind === 'attempt' ? row.problem_id : (row.payload?.problemId as string | undefined);
    if (!pid) continue;
    const k = key(row.user_id, pid);

    // ★reset 은 "행을 지운다" 가 정본이다. 이 한 줄이 없으면 시도 기록만 보고 재계산할 때
    //   사용자가 지운 상태가 그대로 되살아난다 — 이 항목이 존재하는 이유다.
    if (ev.kind === 'problem.reset') { out.delete(k); continue; }

    const cur = out.get(k) ?? { status: 'unsolved', review_state: 'new', next_review: null, attempt_count: 0 };
    if (ev.kind === 'problem.mark_mastered') {
      out.set(k, { status: 'solved', review_state: 'mature',
                   next_review: (row.payload.nextReview as string) ?? null,
                   attempt_count: Math.max(1, cur.attempt_count) });
    } else if (ev.kind === 'problem.skip') {
      // skip 은 next_review 만 민다(행이 없으면 만든다) — problem-state API 의 ON CONFLICT 와 같은 규칙.
      out.set(k, out.has(k)
        ? { ...cur, next_review: (row.payload.nextReview as string) ?? null }
        : { status: 'review', review_state: 'new', next_review: (row.payload.nextReview as string) ?? null, attempt_count: 0 });
    } else if (ev.kind === 'attempt') {
      // ★그 시도가 **일어난 시각** 기준으로 next_review 를 매긴다. 지금 기준으로 매기면
      //   과거 시도가 전부 오늘로 밀려 재계산 결과가 실제와 영영 어긋난다.
      const tr = nextSrsState({ review_state: cur.review_state as never, attempt_count: cur.attempt_count },
                              row.is_correct === true, new Date(row.attempted_at));
      out.set(k, { status: tr.status, review_state: tr.reviewState, next_review: tr.nextReview, attempt_count: cur.attempt_count + 1 });
    }
  }
  return out;
}

/**
 * concept_mastery 재계산. 반환 키는 `${user_id}|${concept_id}`.
 *
 * ★evidence 는 **판단의 산물**이라 시도 기록에서 유도되지 않는다. 이벤트 payload 에 남긴
 *   것을 순서대로 dedupe append 하는 게 유일한 복원 경로다(promoteMastery 와 같은 규칙).
 */
export function replayConceptMastery(events: EventRow[]): Map<string, DerivedMastery> {
  const out = new Map<string, DerivedMastery>();
  const promotes = events.filter((e) => e.kind === 'concept.mastery_promote');
  for (const e of [...promotes].sort((x, y) => ms(x.occurred_at) - ms(y.occurred_at) || Number(x.seq) - Number(y.seq))) {
    const k = key(e.user_id, e.target);
    const cur = out.get(k) ?? { mastery: 'unknown', mastery_evidence: [] };
    const evidence = [...cur.mastery_evidence];
    for (const item of (e.payload.evidence as string[] | undefined) ?? []) {
      if (item && !evidence.includes(item)) evidence.push(item);
    }
    out.set(k, { mastery: (e.payload.to as string) ?? cur.mastery, mastery_evidence: evidence });
  }
  return out;
}

/**
 * 이 대상의 이력이 이벤트 로그로 **온전히 덮이는가**.
 * 덮이지 않으면 재계산 결과를 적용하면 안 된다 — 로그 이전의 사용자 의도를 지우게 된다.
 */
export function isCovered(firstTouchMs: number | undefined, logStartMs: number): boolean {
  return firstTouchMs === undefined || firstTouchMs >= logStartMs;
}
