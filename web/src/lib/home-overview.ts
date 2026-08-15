// 홈 대시보드 데이터 — `index.astro` 가 그리는 모든 것을 서버에서 만든다.
//
// ★왜 서버인가: health·개념그래프·단원요약·추천·오늘의 개념(일별 결정)·삽화 캐시·연속학습일이
//   얽혀 있다. 전부 **파일 읽기와 DB** 다. 클라이언트로 쪼개면 요청이 예닐곱 번 나간다.
// ★삽화 캐시는 **런타임에 읽는다** — 크론이 갱신한 것을 서버 재시작 없이 반영해야 한다.
import { readHealth, readConceptGraph, unitSummary, recommendUnits } from './health.ts';
import { getMasteryMap } from './mastery.ts';
import { getDueProblemCount, getWeeklyActivity } from './activity.ts';
import synthesesIndex from '../data/syntheses-by-concept.json';
import { pickDailyConcept } from './daily-concept.mjs';
import { hasWidget } from './concept-widgets';
import { readFileSync } from 'node:fs';

export async function buildHomeOverview(userId: string | null, now = Date.now()) {
  const health = readHealth();
  const graph = readConceptGraph();
  // 멀티유저: 로그인 사용자의 mastery 를 그래프·단원요약에 오버레이(전역 frontmatter 대신).
  const masteryMap = userId ? await getMasteryMap(userId) : new Map<string, string>();
  const mof = (id: string) => (masteryMap.get(id) ?? 'unknown') as 'unknown' | 'learning' | 'proficient' | 'mastered';
  const graphForUser = { ...graph, nodes: graph.nodes.map((n) => ({ ...n, mastery: masteryMap.get(n.id) ?? 'unknown' })) };
  const units = unitSummary(mof);
  const us = units.byStatus;
  
  // 히어로 「권장 다음 작업」·Due 버튼 — 박제 소스 교체.
  // 옛 fm.suggested_action(초창기 390개념 시절 문자열)·readHealth.dueToday(단일유저
  // frontmatter 전역 next_review 집계) 대신, 사용자별 라이브 데이터로 문구를 만든다.
  const rec = recommendUnits(mof);
  const dueCount = userId ? await getDueProblemCount(userId) : 0;
  const suggestion = (() => {
    const cont = rec.continuing[0];
    const ready = rec.ready[0];
    if (rec.review[0]) return `복습이 기다리는 단원: 「${rec.review[0].label}」 — 기억이 흐려지기 전에 먼저.`;
    if (cont) return `이어서: 「${cont.label}」 (${cont.progressPercent}%)${ready ? ` · 다음 추천: 「${ready.label}」 (선수 충족)` : ''}`;
    if (ready) return `새로 시작하기 좋은 단원: 「${ready.label}」 — 선수 개념이 모두 준비됐습니다.`;
    return '오늘도 한 페이지 — 개념 지도에서 출발점을 골라보세요.';
  })();
  type SynthesisRecent = { slug: string; title: string; created: string | null; origin_concept: string | null; excerpt: string | null };
  const recentSyntheses: SynthesisRecent[] = ((synthesesIndex as any).recent ?? []).slice(0, 5);
  const totalSyntheses: number = (synthesesIndex as any).total ?? 0;
  const leafOf = (p: string | null) => p ? (p.split('/').pop() ?? p).replace(/_/g, ' ') : '';
  
  // 「오늘의 페이지」 히어로 날짜줄 — KST 날짜 + 연속 학습일(streak).
  // 옛 "N번째 페이지"는 2025-01-01 임의 기점이라 사용자와 무관한 숫자였음 → streak 으로 교체.
  // streak 은 오늘부터 역방향 끊기지 않은 학습일(activity.ts). 끊겨 0이면 어색하므로 날짜만 노출.
  const nowKST = new Date(now + 9 * 3600 * 1000);
  const DAYS = ['일', '월', '화', '수', '목', '금', '토'];
  const datePart = `${nowKST.getUTCMonth() + 1}월 ${nowKST.getUTCDate()}일 ${DAYS[nowKST.getUTCDay()]}요일`;
  const streak = userId ? (await getWeeklyActivity(userId)).streak : 0;
  const dateLine = streak >= 1 ? `${datePart} · 연속 ${streak}일째` : datePart;
  // 오늘의 개념 — 전체 개념 풀에서 매일 새로 고른다. 자정(KST)에 바뀐다.
  const todayConcept = pickDailyConcept(graph.nodes, now);
  // 그 개념의 그림(개념별 LLM 생성·캐시). 크론이 미리 채워둠. 없으면 PaperHero 가 일반 곡선 폴백.
  // 런타임 파일 읽기(크론이 갱신한 캐시를 서버 재시작 없이 반영) — readConceptGraph 와 동일 패턴.
  let todaySpec: unknown = null;
  let todayBlurb = '';   // 그 개념의 짧은 인사이트 한 줄(그림과 함께 LLM이 생성·캐시)
  try {
    const illus = JSON.parse(readFileSync(new URL('../data/concept-illustrations.json', import.meta.url), 'utf-8'));
    const entry = todayConcept ? illus[todayConcept.id] : null;
    if (entry) {
      todaySpec = entry;   // PaperHero 의 FigureSpec — 여기선 타입을 끌어오지 않는다(순환 임포트 방지)
      if (typeof entry.blurb === 'string') todayBlurb = entry.blurb;
    }
  } catch { /* 캐시 없음 → 폴백 */ }

  return {
    health, graphForUser, units, us, suggestion, dueCount,
    recentSyntheses, totalSyntheses, dateLine,
    todayConcept: todayConcept && {
      id: todayConcept.id, label: todayConcept.label,
      unit: todayConcept.unit ?? null, domain: todayConcept.domain ?? null,
      hasWidget: hasWidget(todayConcept.id),
    },
    todaySpec, todayBlurb,
    leaf: Object.fromEntries(recentSyntheses.map((s) => [s.slug, leafOf(s.origin_concept)])),
  };
}
