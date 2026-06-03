// 문제 카드 데이터 attribute·props + 두 렌즈(회차별/단원별) 그룹핑 + 필터 옵션 빌더.
// problems/index.astro 와 problems/units.astro 가 공유.
import {
  SUBJECT_ORDER, EXAMTYPE_ORDER, GRADE_ORDER, TIER_ORDER, FORMAT_ORDER,
  FORMAT_LABEL, TIER_BADGE, roundRank, type RoundMeta,
} from './problem-meta';

// astro:content 엔트리의 느슨한 구조 타입 (스키마는 content.config.ts).
export type P = { id: string; data: any };

const subjIdx = (s: string): number => {
  const i = (SUBJECT_ORDER as readonly string[]).indexOf(s);
  return i < 0 ? 99 : i;
};

export function thumbSrc(p: P): string {
  return p.data.problem_image ?? `/problem-images/${p.id.split('/').pop()}.png`;
}

// 필터 아일랜드가 읽는 data-* (모두 단어 1개 → dataset 키와 동일).
export function dataAttrs(p: P): Record<string, string> {
  const s = p.data.source ?? {};
  return {
    'data-examtype': String(s.exam_type ?? ''),
    'data-grade': String(s.grade ?? ''),
    'data-subject': String(s.subject ?? ''),
    'data-tier': String(p.data.killer_tier ?? ''),
    'data-format': String(p.data.format ?? ''),
    'data-unit': String(p.data.unit ?? '').toLowerCase(),
    'data-label': [p.id, p.data.unit ?? '', p.data.exam_intent ?? '']
      .join(' ')
      .toLowerCase(),
  };
}

export function cardProps(p: P) {
  const s = p.data.source ?? {};
  const subj = String(s.subject ?? '');
  const num = s.number ?? '';
  const title = subj === '단일' ? `${num}번` : `${subj} ${num}번`;
  return {
    href: `/problems/${p.id}`,
    thumb: thumbSrc(p),
    title,
    tier: (p.data.killer_tier ?? null) as string | null,
    format: (p.data.format ?? null) as string | null,
    score: (s.score ?? null) as string | number | null,
    cognitive: (p.data.cognitive_type ?? null) as string | null,
    solved: p.data.status === 'solved',
  };
}

// ---- 회차별 렌즈 ----------------------------------------------------------
export type RoundGroup = {
  year: string;
  round: string; // 디렉토리 세그먼트 (예: "고3_9월모의고사")
  meta: RoundMeta;
  problems: P[];
};

export function groupByRound(problems: P[]): Map<string, RoundGroup[]> {
  const byKey = new Map<string, RoundGroup>();
  for (const p of problems) {
    const seg = p.id.split('/');
    const year = seg[0];
    const round = seg[1] ?? seg[0];
    const key = `${year}/${round}`;
    let g = byKey.get(key);
    if (!g) {
      const s = p.data.source ?? {};
      g = {
        year,
        round,
        meta: {
          year,
          agency: String(s.agency ?? ''),
          exam_type: String(s.exam_type ?? ''),
          grade: String(s.grade ?? ''),
          session: String(s.session ?? ''),
        },
        problems: [],
      };
      byKey.set(key, g);
    }
    g.problems.push(p);
  }
  // 회차 내부: 과목 순 → 번호 순
  for (const g of byKey.values()) {
    g.problems.sort((a, b) => {
      const sa = subjIdx(String(a.data.source?.subject ?? ''));
      const sb = subjIdx(String(b.data.source?.subject ?? ''));
      if (sa !== sb) return sa - sb;
      return Number(a.data.source?.number ?? 0) - Number(b.data.source?.number ?? 0);
    });
  }
  // 연도별 묶고 회차 랭크 정렬
  const byYear = new Map<string, RoundGroup[]>();
  for (const g of byKey.values()) {
    if (!byYear.has(g.year)) byYear.set(g.year, []);
    byYear.get(g.year)!.push(g);
  }
  for (const rounds of byYear.values()) {
    rounds.sort((a, b) => {
      const ra = roundRank(a.meta);
      const rb = roundRank(b.meta);
      if (ra.agency !== rb.agency) return ra.agency - rb.agency;
      if (ra.grade !== rb.grade) return ra.grade - rb.grade;
      return ra.month - rb.month;
    });
  }
  // 연도 desc
  return new Map([...byYear.entries()].sort((a, b) => b[0].localeCompare(a[0])));
}

// ---- 단원별 렌즈 ----------------------------------------------------------
export type UnitGroup = { unit: string; problems: P[] };

export function groupByUnit(problems: P[]): UnitGroup[] {
  const byUnit = new Map<string, P[]>();
  for (const p of problems) {
    const u = String(p.data.unit ?? '').trim() || '기타';
    if (!byUnit.has(u)) byUnit.set(u, []);
    byUnit.get(u)!.push(p);
  }
  const groups: UnitGroup[] = [...byUnit.entries()].map(([unit, ps]) => ({ unit, problems: ps }));
  // 기타 맨 뒤, 그 외 문제수 desc
  groups.sort((a, b) => {
    if (a.unit === '기타') return 1;
    if (b.unit === '기타') return -1;
    return b.problems.length - a.problems.length;
  });
  for (const g of groups) g.problems.sort((a, b) => b.id.localeCompare(a.id, 'ko-KR'));
  return groups;
}

// ---- 필터 옵션 (두 렌즈 공통) --------------------------------------------
export type ChipOption = { key: string; label: string; count: number };
export type Axis = { name: string; label: string; attr: string; items: ChipOption[] };

export function buildFilterAxes(problems: P[]): Axis[] {
  const count = (fn: (p: P) => string | undefined | null): Record<string, number> => {
    const m: Record<string, number> = {};
    for (const p of problems) {
      const k = fn(p);
      if (k) m[k] = (m[k] ?? 0) + 1;
    }
    return m;
  };
  const exam = count((p) => p.data.source?.exam_type);
  const grade = count((p) => p.data.source?.grade);
  const subject = count((p) => p.data.source?.subject);
  const tier = count((p) => p.data.killer_tier);
  const format = count((p) => p.data.format);
  const pick = (
    order: readonly string[],
    counts: Record<string, number>,
    label: (k: string) => string,
  ): ChipOption[] =>
    order.filter((k) => counts[k]).map((k) => ({ key: k, label: label(k), count: counts[k] }));

  return [
    { name: 'examtype', label: '시험', attr: 'examtype', items: pick(EXAMTYPE_ORDER, exam, (k) => k) },
    { name: 'grade', label: '학년', attr: 'grade', items: pick(GRADE_ORDER, grade, (k) => k) },
    { name: 'subject', label: '과목', attr: 'subject', items: pick(SUBJECT_ORDER, subject, (k) => k) },
    { name: 'tier', label: '난이도', attr: 'tier', items: pick(TIER_ORDER, tier, (k) => TIER_BADGE[k]?.text ?? k) },
    { name: 'format', label: '유형', attr: 'format', items: pick(FORMAT_ORDER, format, (k) => FORMAT_LABEL[k] ?? k) },
  ];
}
