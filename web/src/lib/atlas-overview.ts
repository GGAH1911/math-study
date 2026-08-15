// 항해 지도(atlas) 데이터 — 좌표·블롭·에지·항로·심도를 **서버에서** 결정적으로 만든다.
//
// ★`buildAtlas` 는 난수 0 의 결정적 빌더다. 클라이언트로 옮기면 개념 그래프 전체를 보내야 하고,
//   같은 배치를 두 곳에서 계산하게 된다 — 화면이 기기마다 미묘하게 달라진다.
import { buildAtlas } from './atlas.ts';
import { recommendUnits, type UnitStatus } from './health.ts';
import { getMasteryMap, getDueConceptIds } from './mastery.ts';
import { getWeeklyActivity, type WeeklyActivity } from './activity.ts';
import synthesesIndex from '../data/syntheses-by-concept.json';

export async function buildAtlasOverview(userId: string | null) {
  // ── 멀티유저: 로그인 사용자의 mastery·due·활동을 항해 지도에 오버레이 ──
  // 비인증이면 전역 그래프값(mof='unknown' 폴백)으로 빈 바다를 그린다(미들웨어가 / 를 302 게이팅하므로
  // 실사용 경로에선 항상 user 존재 — 아래는 SSR 안전 폴백).
  const user = userId;
  const masteryMap = user ? await getMasteryMap(userId!) : new Map<string, string>();
  const mof = (id: string): UnitStatus =>
    (masteryMap.get(id) ?? 'unknown') as UnitStatus;
  const dueIds = user ? await getDueConceptIds(userId!) : new Set<string>();
  
  // 단일 데이터 빌더 — 좌표·블롭·에지·항로·심도 전부 여기서(난수 0, SSR 결정적).
  const atlas = buildAtlas(mof, dueIds);
  
  // 레일 요약: 추천(이어서/준비됨) + 주간 활동.
  const { continuing, ready } = recommendUnits(mof);
  const weekly: WeeklyActivity = user
    ? await getWeeklyActivity(userId!)
    : { days: Array.from({ length: 7 }, () => ({ date: '', count: 0 })), streak: 0 };
  
  // 오늘의 항로 카드: 빌더가 만든 leg 들을 그대로 요약(첫 leg 가 출항 href).
  const route = atlas.route;
  const firstLeg = route[0] ?? null;
  const LEG_GLYPH: Record<string, string> = { review: '⚑', continue: '✕', problem: '★' };
  
  // 어제 남긴 노트(가장 최근 synthesis).
  type SynthesisRecent = { slug: string; title: string; created: string | null; origin_concept?: string | null; excerpt?: string | null };
  const recent: SynthesisRecent[] = ((synthesesIndex as any).recent ?? []).slice(0, 2);
  const recentNote = recent[0] ?? null;
  const leafOf = (p?: string | null) => (p ? (p.split('/').pop() ?? p).replace(/_/g, ' ') : '');
  
  // 심도 범례 수치 — [미답, 답사, 정착, 개척].
  const [dUnknown, dLearning, dProficient, dMastered] = atlas.depthCounts;
  
  // 주간 바: 가장 큰 날 대비 높이 비율. 요일 한글(오래된→오늘).
  const DAYS = ['일', '월', '화', '수', '목', '금', '토'];
  const maxCount = Math.max(1, ...weekly.days.map((d) => d.count));
  const weekBars = weekly.days.map((d) => {
    const wd = d.date ? new Date(`${d.date}T12:00:00+09:00`).getDay() : 0;
    return { label: DAYS[wd], count: d.count, h: Math.round((d.count / maxCount) * 100) };
  });
  const todayIdx = weekBars.length - 1;
  
  // 「오늘의 페이지」 날짜줄 — KST. 지도 좌상 오버레이에 보존(기존 dateLine 로직).
  const nowKST = new Date(Date.now() + 9 * 3600 * 1000);
  const pageNo = Math.floor((nowKST.getTime() - Date.UTC(2025, 0, 1)) / 86400000) + 1;
  const dateLine = `${nowKST.getUTCMonth() + 1}월 ${nowKST.getUTCDate()}일 ${DAYS[nowKST.getUTCDay()]}요일 — ${pageNo}번째 페이지`;
  
  // 항로 카드 부제(leg 별 한 줄). label 은 빌더가 단원명까지 포함.
  const routeMinutes = route.length * 8; // 구간당 ~8분 어림(표시용).

  return {
    atlas, continuing, ready, weekly, route, firstLeg, LEG_GLYPH,
    recent, recentNote,
    recentLeaf: recentNote ? leafOf(recentNote.origin_concept) : '',
  };
}
