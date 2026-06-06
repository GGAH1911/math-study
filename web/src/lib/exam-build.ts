// 교육과정별 랜덤 모의시험 조립.
// 랜덤 대상 = 전체 문제 풀. 각 문제를 **단원**으로 교육과정 영역에 배정하고,
// **양식**(가/나형·공통선택·2028 통합형)별 영역 구성 + **난이도 슬라이더**(0~1)로
// 기초(고1) 혼합 비율과 tier(early/mid/killer) 분포를 조절한다. SSR(prerender=false).
import type { P } from './problem-card';

export const ELECTIVES = ['미적분', '확률과통계', '기하'];
export const FORMATS = [
  { key: '2028', label: '2028 통합형', note: '대수·미적분Ⅰ·확통 (선택 폐지)' },
  { key: 'gongseon', label: '공통+선택', note: '2022~2027 · 공통 22 + 선택 8' },
  { key: 'ganah', label: '가/나형', note: '2021 이전 · 계열별 30' },
] as const;
export type ExamFormat = (typeof FORMATS)[number]['key'];

// ── 단원 → 교육과정 영역 ──────────────────────────────────────────────────
// 대수=前수Ⅰ · 미적분1=前수Ⅱ · 미적분2=초월 미적분(진로선택,2028제외) · 기하(2028제외) · 기초=고1/중등.
const UNIT_AREA: Record<string, string> = {
  '수열': '대수', '삼각함수': '대수', '지수와_로그': '대수', '지수함수와_로그함수': '대수',
  '함수의_극한과_연속': '미적분1', '함수의_극한과_연속성': '미적분1', '미분': '미적분1',
  '적분': '미적분1', '정적분의_활용': '미적분1', '도함수의_활용': '미적분1',
  '도함수의_활용_심화': '미적분1', '합성함수의_미분': '미적분1',
  '수열의_극한': '미적분2', '수열극한': '미적분2', '수열_극한': '미적분2',
  '여러가지함수의_미분': '미적분2', '여러가지함수의_극한': '미적분2', '여러가지_적분법': '미적분2',
  '경우의_수': '확통', '경우의_수_고1': '확통', '확률': '확통', '통계': '확통',
  '이차곡선': '기하', '평면벡터': '기하', '공간도형과_공간벡터': '기하',
};
function areaOf(p: P): string {
  return UNIT_AREA[String(p.data.unit ?? '').trim()] ?? '기초'; // 매핑 외 = 고1/중등 기초
}

// 양식별 수능-level 영역 구성(합 30 기준 비율). 기초는 난이도가 별도로 섞는다.
function formatAreas(format: ExamFormat, option?: string): Record<string, number> {
  if (format === 'ganah') {
    return option === '나형'
      ? { 대수: 11, 미적분1: 11, 확통: 8 }                  // 문과 (= 2028 범위)
      : { 대수: 7, 미적분1: 7, 미적분2: 8, 확통: 8 };       // 이과(가형): 미적분Ⅱ 포함
  }
  if (format === 'gongseon') {
    const sel = option === '확률과통계' ? '확통' : option === '기하' ? '기하' : '미적분2'; // '미적분' 선택 = 미적분Ⅱ
    return { 대수: 11, 미적분1: 11, [sel]: 8 };
  }
  return { 대수: 10, 미적분1: 12, 확통: 8 };                 // 2028 통합형 (대수·미적분Ⅰ·확통)
}

const TIERS = ['early', 'mid', 'killer'] as const;
const TIER_RANK: Record<string, number> = { early: 0, mid: 1, killer: 2 };
const AREA_RANK: Record<string, number> = { 대수: 0, 미적분1: 1, 미적분2: 2, 확통: 3, 기하: 4, 기초: 5 };

// 난이도 d(0~1) → tier 가중치. 쉬움=early多, 어려움=killer多.
function tierWeights(d: number) {
  const l = (a: number, b: number) => a + (b - a) * d;
  return { early: l(0.55, 0.1), mid: l(0.4, 0.4), killer: l(0.05, 0.5) };
}

function pickN<T>(arr: T[], n: number): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a.slice(0, Math.max(0, Math.min(n, a.length)));
}

export type BuildOpts = { format: ExamFormat; option?: string; difficulty: number }; // difficulty 0..1

export function buildRandomExam(problems: P[], opts: BuildOpts): P[] {
  const TOTAL = 30;
  const tw = tierWeights(opts.difficulty);
  const nBase = Math.round(TOTAL * 0.35 * (1 - opts.difficulty));  // 기초(고1) 혼합 — 쉬울수록↑
  const nSusu = TOTAL - nBase;
  const areas = formatAreas(opts.format, opts.option);
  const areaSum = Object.values(areas).reduce((a, b) => a + b, 0);

  const used = new Set<string>();
  const out: P[] = [];
  const drawTierWeighted = (area: string, n: number) => {
    if (n <= 0) return;
    const byTier: Record<string, P[]> = { early: [], mid: [], killer: [] };
    for (const p of problems) {
      if (areaOf(p) !== area || used.has(p.id)) continue;
      (byTier[String(p.data.killer_tier ?? 'mid')] ?? byTier.mid).push(p);
    }
    for (const t of TIERS) {
      for (const p of pickN(byTier[t], Math.round(n * tw[t]))) { out.push(p); used.add(p.id); }
    }
  };

  for (const [area, c] of Object.entries(areas)) drawTierWeighted(area, Math.round(nSusu * c / areaSum));
  drawTierWeighted('기초', nBase);

  // 라운딩·풀부족 보충 — 이 양식의 영역(+기초)에서 tier 무관 채움.
  const eligible = new Set([...Object.keys(areas), '기초']);
  if (out.length < TOTAL) {
    const rest = problems.filter((p) => eligible.has(areaOf(p)) && !used.has(p.id));
    for (const p of pickN(rest, TOTAL - out.length)) { out.push(p); used.add(p.id); }
  }

  // 영역 순 → 난이도 순. 번호는 라우트에서 1..N 재부여.
  out.sort((a, b) => {
    const ra = AREA_RANK[areaOf(a)] ?? 9, rb = AREA_RANK[areaOf(b)] ?? 9;
    if (ra !== rb) return ra - rb;
    return (TIER_RANK[a.data.killer_tier ?? 'mid'] ?? 1) - (TIER_RANK[b.data.killer_tier ?? 'mid'] ?? 1);
  });
  return out.slice(0, TOTAL);
}
