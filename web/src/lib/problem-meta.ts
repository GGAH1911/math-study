// 문제 브라우저 · 모의시험 공유 상수/헬퍼.
// 흩어져 있던 tier 배지(concepts/[...slug].astro)·회차 정렬(dev/rounds.astro)을 한 곳으로.

export const EXAMTYPE_ORDER = ['수능', '모의평가', '모의고사'] as const;
// 가형·나형 = 2021학년도 이전 수능/모평의 계열별 단일트랙 (선택과목 체제 이전).
export const SUBJECT_ORDER = ['공통', '미적분', '확률과통계', '기하', '가형', '나형', '단일'] as const;
export const ELECTIVES = ['미적분', '확률과통계', '기하'] as const; // 선택과목 (회차당 택1, 8문항)
export const GRADE_ORDER = ['고1', '고2', '고3'] as const;
export const TIER_ORDER = ['early', 'mid', 'killer'] as const; // 코퍼스엔 high 미사용
export const FORMAT_ORDER = ['choice', 'numeric'] as const;

export const FORMAT_LABEL: Record<string, string> = {
  choice: '객관식',
  numeric: '단답형',
  descriptive: '서술형',
};

// 난이도 배지 — 상/중/하 3단(데이터 키는 early/mid/killer 유지, 표시만 한글).
// 난이도순: killer(최고난도)=상, mid=중, early=하. cls 색도 난이도 직관에 맞춤(상=rose, 하=중립).
export const TIER_BADGE: Record<string, { text: string; cls: string }> = {
  killer: { text: '상', cls: 'bg-rose-500/20 text-rose-300 border-rose-500/40' },
  high: { text: '상', cls: 'bg-amber-500/20 text-amber-300 border-amber-500/40' }, // 레거시 슬롯(미사용)
  mid: { text: '중', cls: 'bg-sky-500/20 text-sky-300 border-sky-500/40' },
  early: { text: '하', cls: 'bg-zinc-600/30 text-zinc-300 border-zinc-600' },
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

// 연도 표기를 명시적으로: 수능·모평은 학년도(대학입학 기준), 모의고사(교육청 학평)는
// 시행연도. 같은 'year' 숫자라도 종류에 따라 가리키는 게 다르므로 라벨에 확실히 박는다.
//   수능/모평 → "2026학년도"   ·   모의고사 → "2026년"
export function yearLabel(year: string | number, examType: string): string {
  return examType === '모의고사' ? `${year}년` : `${year}학년도`;
}

// 표시 제목: "2026학년도 대학수학능력시험", "2026학년도 고3 9월 모의평가", "2026년 고1 3월 모의고사".
export function roundTitle(m: RoundMeta): string {
  const yl = yearLabel(m.year, m.exam_type);
  // 수능 본수능은 정식 명칭으로(예시문항은 별도 — 아래 일반 포맷 사용).
  if (m.exam_type === '수능' && !/예시/.test(m.session)) return `${yl} 대학수학능력시험`;
  const parts = [yl];
  if (m.grade) parts.push(m.grade);
  if (m.session && m.session !== '?') parts.push(m.session);
  parts.push(m.exam_type);
  return parts.join(' ');
}
