// 개념 대시보드 데이터 — `concepts/index` 가 그리는 **모든 것**을 서버에서 만든다.
//
// ★왜 전부 서버인가: 이 화면은 목록이 아니라 대시보드다. 여섯 가지가 합쳐진다 —
//   ① 사용자별 mastery(DB) ② 단원 진행도 ③ 추천 3종(이어서·다음·복습) ④ 개념 요약(빌드 산출물)
//   ⑤ 단원별 기출 수(빌드 산출물) ⑥ 위젯 유무. 클라이언트로 옮기면 요청이 여섯 번 나가고,
//   단원↔스포크 매칭처럼 **파일 경로 의미에 기대는 로직**까지 브라우저로 옮겨야 한다.
//
// ★★단원↔스포크 매칭은 content id 의 **경로 부모**로만 한다. graph 의 `home_unit` 에 기대면
//   빌드 스크립트(Node readdir)와 Astro 가 한글 파일명을 서로 다른 유니코드 정규화로 디코딩해
//   일부 스포크가 "기타(단원 미연결)"로 떨어진다. 양쪽 다 NFC 로 통일한다.
//   (파일 레이아웃 `<domain>/<grade>/<unit>/<spoke>` 이 권위 있는 소속이다.)
import { getCollection } from 'astro:content';
import {
  DOMAIN_ORDER, DOMAIN_COLOR, TYPE_LABEL_KO, GRADE_ORDER, MASTERY_ORDER, MASTERY_LABEL_KO,
} from './concept-meta';
import { computeUnitProgress, recommendUnits } from './health.ts';
import { getMasteryMap } from './mastery.ts';
import { hasWidget } from './concept-widgets';
import summariesJson from '../data/concept-summaries.json';
import problemsByConcept from '../data/problems-by-concept.json';

/** 트랙 프리셋 (grade 필터 set 설정용). */
export const TRACKS = [
  { key: '미적분', grades: ['수학1', '수학2', '미적분'] },
  { key: '확통', grades: ['수학1', '수학2', '확률과통계'] },
  { key: '기하', grades: ['수학1', '수학2', '기하'] },
  { key: '고1', grades: ['고1'] },
  { key: '중등', grades: ['중1', '중2', '중3'] },
];

export async function buildConceptsOverview(userId: string | null) {
  const summaries: Record<string, string> = (summariesJson as any).summaries ?? {};
  
  const concepts = await getCollection('concepts');
  // 멀티유저: 로그인 사용자의 mastery 를 단원진행·per-concept 표시에 사용(전역 frontmatter 대신).
  const masteryMap = userId ? await getMasteryMap(userId) : new Map<string, string>();
  const mof = (id: string) => (masteryMap.get(id) ?? 'unknown') as 'unknown' | 'learning' | 'proficient' | 'mastered';
  const cmOf = (id: string) => masteryMap.get(id) ?? 'unknown';
  // 단원 카드에 표시할 롤업 진행도 (unitId → UnitProgress).
  const unitProgress = new Map(computeUnitProgress(mof).map((u) => [u.unitId, u] as const));
  
  // 상단 진행도 추천 행 (이어서학습·다음추천·복습) — 빈 행은 숨김.
  const rec = recommendUnits(mof);
  const recRows = [
    { icon: '▶', label: '이어서 학습', units: rec.continuing },
    { icon: '✦', label: '다음 추천', units: rec.ready },
    { icon: '↻', label: '복습', units: rec.review },
  ].filter((r) => r.units.length > 0);
  
  // 단원별 기출 수 (problems-by-concept: direct+propagated).
  const byConcept: Record<string, any[]> = (problemsByConcept as any).byConcept ?? {};
  const problemCountOf = (unitId: string) => (byConcept[unitId]?.length ?? 0);
  
  // 트랙 프리셋 (grade 필터 set 설정용).
  const tracks = [
    { key: '미적분', grades: ['수학1', '수학2', '미적분'] },
    { key: '확통', grades: ['수학1', '수학2', '확률과통계'] },
    { key: '기하', grades: ['수학1', '수학2', '기하'] },
    { key: '고1', grades: ['고1'] },
    { key: '중등', grades: ['중1', '중2', '중3'] },
  ];
  
  const byMastery = { unknown: 0, learning: 0, proficient: 0, mastered: 0 } as Record<string, number>;
  for (const c of concepts) byMastery[cmOf(c.id)]++;
  const byType = { unit: 0, definition: 0, theorem: 0, lemma: 0, example: 0 } as Record<string, number>;
  for (const c of concepts) byType[c.data.concept_type]++;
  const byGrade: Record<string, number> = {};
  for (const c of concepts) if (c.data.grade) byGrade[c.data.grade] = (byGrade[c.data.grade] ?? 0) + 1;
  const byDomain: Record<string, number> = {};
  for (const c of concepts) {
    const d = c.data.domain ?? 'misc';
    byDomain[d] = (byDomain[d] ?? 0) + 1;
  }
  
  // Group: domain → unit → [unit card, then spokes belonging to that unit].
  // Spokes without a resolvable home unit fall into a per-domain "기타" bucket
  // shown after all units.
  type C = (typeof concepts)[number];
  const byDomainNodes: Record<string, C[]> = {};
  for (const c of concepts) {
    const d = c.data.domain ?? 'misc';
    (byDomainNodes[d] ??= []).push(c);
  }
  const orderedDomains = [
    ...DOMAIN_ORDER.filter((d) => byDomainNodes[d]),
    ...Object.keys(byDomainNodes).filter((d) => !DOMAIN_ORDER.includes(d as any)),
  ];
  
  type Group = { unitId: string | null; unit: C | null; spokes: C[] };
  function groupByUnit(items: C[]): Group[] {
    const unitsHere = items.filter((c) => c.data.concept_type === 'unit');
    unitsHere.sort((a, b) => a.id.localeCompare(b.id, 'ko-KR'));
    const groups: Group[] = unitsHere.map((u) => ({ unitId: u.id, unit: u, spokes: [] }));
    // 단원↔스포크 매칭은 content-collection c.id 의 경로 부모로만 한다.
    // graph 의 home_unit 에 기대면 build-script(Node readdir)와 Astro 가 한글
    // 파일명을 서로 다른 유니코드 정규화로 디코딩해 일부 스포크가 매칭에 실패하고
    // "기타(단원 미연결)" 로 떨어진다. 양쪽 다 NFC 로 통일해 같은 파일을 가리키는
    // id 가 항상 일치하게 한다. (파일 레이아웃 <domain>/<grade>/<unit>/<spoke>
    // 이 권위 있는 소속이므로 경로 부모 = 소속 단원.)
    const idxByUnit = new Map(groups.map((g, i) => [g.unitId!.normalize('NFC'), i]));
    const orphans: C[] = [];
    for (const c of items) {
      if (c.data.concept_type === 'unit') continue;
      const home = c.id.includes('/') ? c.id.slice(0, c.id.lastIndexOf('/')).normalize('NFC') : null;
      if (home && idxByUnit.has(home)) {
        groups[idxByUnit.get(home)!].spokes.push(c);
      } else {
        orphans.push(c);
      }
    }
    for (const g of groups) {
      g.spokes.sort((a, b) => {
        // definitions first (학습 시작점), then theorems, lemmas, examples
        const order = { definition: 0, theorem: 1, lemma: 2, example: 3 } as Record<string, number>;
        const ta = order[a.data.concept_type] ?? 9;
        const tb = order[b.data.concept_type] ?? 9;
        if (ta !== tb) return ta - tb;
        return a.id.localeCompare(b.id, 'ko-KR');
      });
    }
    if (orphans.length) {
      orphans.sort((a, b) => a.id.localeCompare(b.id, 'ko-KR'));
      groups.push({ unitId: null, unit: null, spokes: orphans });
    }
    return groups;
  }
  
  const groupedByDomain: Record<string, Group[]> = {};
  for (const d of orderedDomains) groupedByDomain[d] = groupByUnit(byDomainNodes[d]);
  
  function cardProps(c: C, options: { emphasized?: boolean } = {}) {
    const path = c.id.includes('/') ? c.id.slice(0, c.id.lastIndexOf('/')) : '';
    const label = (c.id.split('/').pop() ?? c.id).replace(/_/g, ' ');
    const typeKo = TYPE_LABEL_KO[c.data.concept_type] ?? c.data.concept_type;
    const mlvl = cmOf(c.id);
    const masteryKo = MASTERY_LABEL_KO[mlvl] ?? mlvl;
    const up = c.data.concept_type === 'unit' ? unitProgress.get(c.id) : undefined;
    const pc = c.data.concept_type === 'unit' ? problemCountOf(c.id) : 0;
    return {
      href: `/concepts/${c.id}`,
      graphHref: `/graph?highlight=${encodeURIComponent(c.id)}`,
      title: label,
      subtitle: path,
      emphasized: options.emphasized,
      description: summaries[c.id],
      progress: up ? { percent: up.progressPercent, status: up.status } : undefined,
      practice: pc > 0 ? { count: pc, href: `/problems?q=${encodeURIComponent(c.data.unit ?? label)}` } : undefined,
      chips: [
        { label: masteryKo, class: `chip-mastery-${mlvl}` },
        { label: typeKo, class: '' },
        ...(c.data.grade ? [{ label: c.data.grade, class: '' }] : []),
        ...(hasWidget(c.id) ? [{ label: '🔭 인터랙티브', class: 'chip-interactive' }] : []),
      ],
    };
  }
  
  function dataAttrs(c: C) {
    const label = (c.id.split('/').pop() ?? c.id).replace(/_/g, ' ');
    return {
      'data-mastery': cmOf(c.id),
      'data-domain': c.data.domain ?? 'misc',
      'data-grade': c.data.grade ?? '',
      'data-type': c.data.concept_type,
      'data-label': label.toLowerCase(),
      'data-id': c.id.toLowerCase(),
      'data-unit': (c.data.unit ?? '').toLowerCase(),
      'data-interactive': hasWidget(c.id) ? '1' : '',
    };
  }
  
  // Used by the filter island to populate option chips. Keeps order
  // consistent with the rest of the UI.
  const filterOptions = {
    masteries: MASTERY_ORDER.map((m) => ({
      key: m,
      label: MASTERY_LABEL_KO[m] ?? m,
      count: byMastery[m] ?? 0,
    })),
    domains: orderedDomains.map((d) => ({
      key: d,
      label: d === 'misc' ? '기타' : d,
      color: DOMAIN_COLOR[d] ?? '#71717a',
      count: byDomain[d] ?? 0,
    })),
    grades: GRADE_ORDER.filter((g) => byGrade[g]).map((g) => ({
      key: g,
      label: g,
      count: byGrade[g],
    })),
  };

  return {
    total: concepts.length,
    byType, byMastery, byGrade, byDomain,
    filterOptions,
    tracks: TRACKS,
    interactiveCount: concepts.filter((c) => hasWidget(c.id)).length,
    recRows: recRows.map((r) => ({
      icon: r.icon, label: r.label,
      units: r.units.slice(0, 12).map((u) => ({
        unitId: u.unitId, label: u.label, grade: u.grade, domain: u.domain,
        progressPercent: u.progressPercent, status: u.status,
      })),
    })),
    domains: orderedDomains.map((d) => ({
      domain: d,
      label: d === 'misc' ? '기타' : d,
      color: DOMAIN_COLOR[d] ?? '#71717a',
      nodeCount: byDomainNodes[d].length,
      unitCount: groupedByDomain[d].filter((g) => g.unit).length,
      groups: groupedByDomain[d].map((g) => ({
        unitId: g.unitId,
        unit: g.unit ? { card: cardProps(g.unit, { emphasized: true }), attrs: dataAttrs(g.unit) } : null,
        spokes: g.spokes.map((c) => ({ card: cardProps(c), attrs: dataAttrs(c) })),
      })),
    })),
  };
}
