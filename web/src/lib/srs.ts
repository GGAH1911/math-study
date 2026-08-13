// Spaced-repetition scheduler — small Leitner-style ladder tuned for high-
// school math practice. Three boxes:
//   new      — never solved correctly
//   learning — solved once or twice, still consolidating
//   mature   — confidently solved multiple times
//
// On a correct answer we promote one box and push next_review forward by an
// interval that doubles each level. On an incorrect answer we demote to
// new and queue it for *tomorrow* so the student can confront it again
// while the failure is still fresh (not same-day to avoid spaced repetition
// turning into rote re-reading).
export type ReviewState = 'new' | 'learning' | 'mature';
export type Status = 'unsolved' | 'solved' | 'review';

// 표시용 한글 라벨 — 코드/DB 값(위 enum)은 그대로 두고 UI 표시에만 매핑.
export const REVIEW_STATE_LABEL_KO: Record<string, string> = {
  new: '신규', learning: '학습 중', mature: '익힘',
};
export const STATUS_LABEL_KO: Record<string, string> = {
  unsolved: '미풀이', solved: '완료', review: '복습',
};

export interface SrsTransition {
  status: Status;
  reviewState: ReviewState;
  nextReview: string;       // YYYY-MM-DD
  intervalDays: number;
}

// Compute next_review off the *local* calendar day, not UTC. A KST (UTC+9)
// user submitting between local 00:00–08:59 is still on the previous UTC day,
// so `.toISOString().slice(0,10)` would emit yesterday's date and
// todayPlusDays(1) would collapse "tomorrow" into "today" (off-by-one vs a
// local-time `current_date` due check). Stepping the local calendar date and
// formatting the local Y-M-D keeps generation and the due-today comparison in
// the same timezone.
// ★`from` 을 받는다: 이벤트 재생(problem_attempts 로부터 상태 재계산)은 **그 시도가 있었던
//   시각** 기준으로 next_review 를 매겨야 한다. 호출 시각을 쓰면 과거 시도를 재생할 때마다
//   전부 오늘 기준으로 밀려, 재계산 결과가 실제 상태와 영영 어긋난다.
function todayPlusDays(days: number, from: Date = new Date()): string {
  const d = new Date(from);
  d.setHours(0, 0, 0, 0);
  d.setDate(d.getDate() + days);
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
}

/**
 * Decide the next learning state after an attempt.
 *
 * @param current   the row in problem_state before this attempt (or null
 *                  for a brand-new problem)
 * @param correct   whether the student got the answer right
 */
export function nextSrsState(
  current: { review_state: ReviewState; attempt_count: number } | null,
  correct: boolean,
  /** 이 시도가 **일어난** 시각. 생략하면 지금 — 재생할 때는 반드시 넘겨라. */
  at: Date = new Date(),
): SrsTransition {
  const prev: ReviewState = current?.review_state ?? 'new';

  if (!correct) {
    // Reset ladder. Tomorrow's queue.
    return {
      status: 'review',
      reviewState: 'new',
      nextReview: todayPlusDays(1, at),
      intervalDays: 1,
    };
  }

  // Correct → promote one rung.
  let nextLevel: ReviewState;
  let interval: number;
  if (prev === 'new')        { nextLevel = 'learning'; interval = 3; }
  else if (prev === 'learning') { nextLevel = 'mature';  interval = 10; }
  else                         { nextLevel = 'mature';  interval = 30; }

  return {
    status: 'solved',
    reviewState: nextLevel,
    nextReview: todayPlusDays(interval, at),
    intervalDays: interval,
  };
}

/**
 * Loose equivalence — handles "①" vs "1", whitespace, fullwidth/halfwidth.
 * Used to grade attempts since answers are entered free-form in the UI.
 */
export function answersMatch(given: string, expected: string): boolean {
  const norm = (s: string) =>
    s.trim()
      .replace(/\s+/g, '')
      // ① ② ③ ④ ⑤ → 1..5
      .replace(/[①②③④⑤]/g, (c) => String('①②③④⑤'.indexOf(c) + 1))
      // fullwidth digits → ascii
      .replace(/[０-９]/g, (c) => String.fromCharCode(c.charCodeAt(0) - 0xFEE0))
      .toLowerCase();
  return norm(given) === norm(expected) && norm(given) !== '';
}
