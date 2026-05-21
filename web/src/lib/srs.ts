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

const DAY_MS = 86_400_000;

export interface SrsTransition {
  status: Status;
  reviewState: ReviewState;
  nextReview: string;       // YYYY-MM-DD
  intervalDays: number;
}

function todayPlusDays(days: number): string {
  return new Date(Date.now() + days * DAY_MS).toISOString().slice(0, 10);
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
): SrsTransition {
  const prev: ReviewState = current?.review_state ?? 'new';

  if (!correct) {
    // Reset ladder. Tomorrow's queue.
    return {
      status: 'review',
      reviewState: 'new',
      nextReview: todayPlusDays(1),
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
    nextReview: todayPlusDays(interval),
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
