// 문제 브라우저 · 모의시험 공유 상수/헬퍼.
// 흩어져 있던 tier 배지(concepts/[...slug].astro)·회차 정렬(dev/rounds.astro)을 한 곳으로.

export const EXAMTYPE_ORDER = ['수능', '모의평가', '모의고사'] as const;
export const SUBJECT_ORDER = ['공통', '미적분', '확률과통계', '기하', '단일'] as const;
export const ELECTIVES = ['미적분', '확률과통계', '기하'] as const; // 선택과목 (회차당 택1, 8문항)
export const GRADE_ORDER = ['고1', '고2', '고3'] as const;
export const TIER_ORDER = ['early', 'mid', 'killer'] as const; // 코퍼스엔 high 미사용
export const FORMAT_ORDER = ['choice', 'numeric'] as const;

export const FORMAT_LABEL: Record<string, string> = {
  choice: '객관식',
  numeric: '단답형',
  descriptive: '서술형',
};

// 난이도 배지 — concepts/[...slug].astro 의 TIER_LABEL 을 이전·공유.
export const TIER_BADGE: Record<string, { text: string; cls: string }> = {
  killer: { text: '킬러', cls: 'bg-rose-500/20 text-rose-300 border-rose-500/40' },
  high: { text: 'high', cls: 'bg-amber-500/20 text-amber-300 border-amber-500/40' },
  mid: { text: 'mid', cls: 'bg-sky-500/20 text-sky-300 border-sky-500/40' },
  early: { text: 'early', cls: 'bg-zinc-600/30 text-zinc-300 border-zinc-600' },
};

export const MONTH_ORDER = ['3월', '4월', '5월', '6월', '7월', '9월', '10월', '11월'];

export type RoundMeta = {
  year: string;
  agency: string;
  exam_type: string;
  grade: string;
  session: string;
};

// 회차 정렬 랭크 — dev/rounds.astro 레시피: 연도 desc → 수능>평가원>교육청 → 학년 → 시행월.
export function roundRank(m: RoundMeta): { agency: number; grade: number; month: number } {
  const agency = m.exam_type === '수능' ? 0 : m.agency === '평가원' ? 1 : 2;
  const grade = m.grade === '고1' ? 1 : m.grade === '고2' ? 2 : m.grade === '고3' ? 3 : 0;
  const month = MONTH_ORDER.indexOf(m.session);
  return { agency, grade, month: month < 0 ? 99 : month };
}

// 표시 제목: "2025 고3 9월 모의평가", "2025 수능", "2025 고1 3월 모의고사".
export function roundTitle(m: RoundMeta): string {
  const parts = [m.year];
  if (m.grade) parts.push(m.grade);
  if (m.session && m.session !== '?') parts.push(m.session);
  parts.push(m.exam_type);
  return parts.join(' ');
}
