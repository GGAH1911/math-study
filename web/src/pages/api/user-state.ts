// 사용자 학습 상태 — `GET /api/user-state` → 여러 화면이 공유하는 한 벌
//
// ★왜 하나로 묶나: `index`·`atlas`·`graph`·`paths`·`account` 가 **같은 것들**을 각자 읽고 있었다
//   (`getMasteryMap` 은 다섯 페이지 전부). 페이지마다 엔드포인트를 만들면 같은 쿼리가 다섯 벌
//   생기고, 한 곳만 고치면 화면끼리 값이 어긋난다.
//
// ★`Map`·`Set` 은 JSON 이 아니다 — 배열/객체로 평탄화해 보낸다. 클라이언트가 다시 Map 으로
//   만들 필요도 없다(조회는 객체로 충분하다).
//
// ★사용자별이므로 `no-store`. 캐시되면 남의 진도가 보인다.
import type { APIRoute } from 'astro';
import { getMasteryMap, getDueConceptIds, getMasteryCounts } from '../../lib/mastery.ts';
import { getWeeklyActivity, getDueProblemCount } from '../../lib/activity.ts';

export const prerender = false;

const json = (b: unknown, s: number) =>
  new Response(JSON.stringify(b), {
    status: s,
    headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
  });

export const GET: APIRoute = async ({ locals }) => {
  const userId = (locals as { user?: { id?: string } }).user?.id ?? null;
  // 미인증은 미들웨어가 401 로 막는다. 여기 오면 사용자가 있다 — 다만 방어적으로 빈 상태를 준다.
  if (!userId) return json({ mastery: {}, dueConceptIds: [], dueProblemCount: 0, weekly: null, masteryCounts: {} }, 200);

  try {
    const [mastery, dueIds, counts, weekly, dueProblems] = await Promise.all([
      getMasteryMap(userId),
      getDueConceptIds(userId),
      getMasteryCounts(userId),
      getWeeklyActivity(userId),
      getDueProblemCount(userId),
    ]);
    return json({
      mastery: Object.fromEntries(mastery),   // Map → 객체
      dueConceptIds: [...dueIds],             // Set → 배열
      masteryCounts: counts,
      weekly,
      dueProblemCount: dueProblems,
    }, 200);
  } catch (e) {
    console.error('[user-state]', e);
    return json({ error: 'user state failed' }, 500);
  }
};
