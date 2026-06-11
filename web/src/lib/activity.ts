// 사용자별 학습 활동 집계 — 항해 계기판의 "이번 주 항해"·"연속 항해" 게이지 소스.
// problem_attempts 를 Asia/Seoul 날짜로 환산해 집계한다(서버 TZ 와 무관하게 KST 하루 경계).
import sql from './db.ts';

export type WeeklyActivity = {
  // 최근 7일(오래된→오늘 순). count = 그 날 푼 문제 시도 수.
  days: { date: string; count: number }[];
  // 오늘부터 역방향으로 끊기지 않은 활동일 수. 오늘 0건이면 어제부터 센다(오늘은 아직 진행 중이므로).
  streak: number;
};

// problem_attempts 의 KST 날짜별 시도 수. 한 번의 쿼리로 충분한 범위(연속일 계산 위해 넉넉히 90일)를 긁어
// 메모리에서 7일 창 + 연속일을 계산한다(빈 날은 0 으로 채워야 하므로 SQL GROUP BY 만으론 부족).
export async function getWeeklyActivity(userId: string): Promise<WeeklyActivity> {
  const rows = await sql<{ day: string; n: number }[]>`
    SELECT to_char((attempted_at AT TIME ZONE 'Asia/Seoul')::date, 'YYYY-MM-DD') AS day,
           count(*)::int AS n
      FROM problem_attempts
     WHERE user_id = ${userId}
       AND attempted_at >= (now() AT TIME ZONE 'Asia/Seoul')::date - 89
     GROUP BY 1
  `;
  const byDay = new Map<string, number>();
  for (const r of rows) byDay.set(r.day, r.n);

  // 기준 '오늘'(KST). new Date 의 로컬 TZ 에 의존하지 않도록 ko-KR Asia/Seoul 포맷터로 YYYY-MM-DD 추출.
  const kstFmt = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Asia/Seoul', year: 'numeric', month: '2-digit', day: '2-digit',
  });
  const todayStr = kstFmt.format(new Date()); // en-CA → 'YYYY-MM-DD'
  // 날짜 산술은 정오 UTC 앵커로 DST/경계 흔들림 없이 일 단위 가감.
  const anchor = new Date(`${todayStr}T12:00:00Z`);
  const dayStrAt = (offset: number): string => {
    const d = new Date(anchor.getTime() + offset * 86400000);
    return kstFmt.format(d);
  };

  // 최근 7일 창: offset -6 … 0.
  const days: { date: string; count: number }[] = [];
  for (let i = 6; i >= 0; i--) {
    const date = dayStrAt(-i);
    days.push({ date, count: byDay.get(date) ?? 0 });
  }

  // 연속일: 오늘이 0이면 어제부터 시작(오늘은 미완), 1+ 이면 오늘부터. 0 만나면 중단.
  // 데이터 창(90일) 밖은 어차피 0 으로 끊긴다 — 그 안에서만 센다.
  let streak = 0;
  const start = (byDay.get(todayStr) ?? 0) > 0 ? 0 : -1;
  for (let i = start; i > -90; i--) {
    if ((byDay.get(dayStrAt(i)) ?? 0) > 0) streak++;
    else break;
  }
  return { days, streak };
}
