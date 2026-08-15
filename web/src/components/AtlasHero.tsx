// 항해 지도 히어로 — Phase 3 C그룹. 데이터는 `/api/atlas`(좌표·항로·주간활동·심도).
//
// ★파생값(주간 바 높이·날짜줄·심도 범례)은 **여기서** 만든다 — 서버가 계산해도 되지만
//   표시 전용이라 페이로드만 늘어난다. 원본과 같은 규칙을 그대로 옮겼다.
import { useJsonOnce } from '../lib/content-entry.ts';
import AtlasMap from './AtlasMap.tsx';

type Leg = { kind: string; label: string; href: string };
type Atlas = { depthCounts: [number, number, number, number]; route: Leg[] };
type Data = {
  atlas: Atlas;
  route: Leg[]; firstLeg: Leg | null; LEG_GLYPH: Record<string, string>;
  weekly: { days: Array<{ date: string; count: number }>; streak: number };
  recentNote: { slug: string; title: string; origin_concept?: string | null } | null;
  recentLeaf: string;
};

const DAYS = ['일', '월', '화', '수', '목', '금', '토'];

export default function AtlasHero() {
  const s = useJsonOnce<Data>('/api/atlas');
  if (s.status === 'error') {
    return <div className="atlas-col grid place-items-center text-sm text-[color:var(--color-muted)]">항해 지도를 불러오지 못했습니다 — {s.message}</div>;
  }
  if (s.status !== 'ready') {
    return <div className="atlas-col grid place-items-center text-sm text-[color:var(--color-muted)]">해도를 펼치는 중…</div>;
  }
  const d = s.data;
  const { route, firstLeg, weekly } = d;
  const [dUnknown, dLearning, dProficient, dMastered] = d.atlas.depthCounts;

  // 주간 바 — 가장 큰 날 대비 높이 비율.
  const maxCount = Math.max(1, ...weekly.days.map((x) => x.count));
  const weekBars = weekly.days.map((x) => {
    const wd = x.date ? new Date(`${x.date}T12:00:00+09:00`).getDay() : 0;
    return { label: DAYS[wd], count: x.count, h: Math.round((x.count / maxCount) * 100) };
  });
  const todayIdx = weekBars.length - 1;

  // 날짜줄 — KST. 「N번째 페이지」는 2025-01-01 기점(원본 유지).
  const nowKST = new Date(Date.now() + 9 * 3600 * 1000);
  const pageNo = Math.floor((nowKST.getTime() - Date.UTC(2025, 0, 1)) / 86400000) + 1;
  const dateLine = `${nowKST.getUTCMonth() + 1}월 ${nowKST.getUTCDate()}일 ${DAYS[nowKST.getUTCDay()]}요일 — ${pageNo}번째 페이지`;
  const routeMinutes = route.length * 8;   // 구간당 ~8분 어림(표시용)

  return (
    <>
      <div className="atlas-col">
        <AtlasMap atlas={d.atlas as never} />
        <p className="atlas-dateline font-hand">{dateLine}</p>
      </div>

      <aside className="nav-rail" id="navRail" aria-label="항해 계기판">
        <button className="nav-handle" type="button" id="navHandle" aria-expanded="false">⌃ 항해 계기판</button>

        <div className="nav-gauge nav-route">
          <div className="nav-t">{route.length > 0 ? `오늘의 항로 — ${route.length}구간 · 약 ${routeMinutes}분` : '오늘의 항로'}</div>
          {route.length > 0 ? (
            <div className="nav-s">
              {route.map((leg, i) => <span className="nav-leg-line" key={i}>{d.LEG_GLYPH[leg.kind] ?? '·'} {leg.label}</span>)}
            </div>
          ) : (
            <div className="nav-s">지도에서 시작할 단원을 골라보세요.</div>
          )}
          {firstLeg
            ? <a className="nav-depart" href={firstLeg.href}>⛵ 출항</a>
            : <a className="nav-depart" href="/graph">◈ 지도 둘러보기</a>}
        </div>

        <div className="nav-gauge">
          <div className="nav-t-sm">연속 항해 <span className="nav-streak">{weekly.streak}일</span></div>
          <div className="nav-week" aria-label="최근 7일 학습량">
            {weekBars.map((b, i) => (
              <span key={i} className={`nav-bar${i === todayIdx ? ' is-today' : ''}`}
                    style={{ height: `${Math.max(b.count > 0 ? 14 : 6, b.h)}%` }}
                    title={`${b.label} · ${b.count}문제`} />
            ))}
          </div>
          <div className="nav-week-labels" aria-hidden="true">
            {weekBars.map((b, i) => <span key={i}>{b.label}</span>)}
          </div>
        </div>

        <a className="nav-gauge nav-gauge-link" href="/exam">
          <div className="nav-t-sm">모의시험 <span className="nav-pill">87회차</span></div>
          <div className="nav-s">기출·모평 회차로 실전 점검 →</div>
        </a>

        {d.recentNote ? (
          <a className="nav-gauge nav-gauge-link" href={`/syntheses/${encodeURIComponent(d.recentNote.slug)}`}>
            <div className="nav-t-sm">최근 남긴 노트</div>
            <div className="nav-s nav-note"><b>{d.recentNote.title}</b>{d.recentLeaf && <> — {d.recentLeaf}</>} →</div>
          </a>
        ) : (
          <a className="nav-gauge nav-gauge-link" href="/syntheses">
            <div className="nav-t-sm">학습 노트</div>
            <div className="nav-s">채팅에서 저장한 영구 노트 →</div>
          </a>
        )}

        <div className="nav-block">
          <h5>단원 심도 — 잉크로 칠한 만큼 내 것</h5>
          <div className="nav-depth-legend">
            <div className="row"><span className="nav-dl nav-dl-0" />미답 — 윤곽만<span className="nav-dl-n">{dUnknown}</span></div>
            <div className="row"><span className="nav-dl nav-dl-1" />답사 — 연필 해칭<span className="nav-dl-n">{dLearning}</span></div>
            <div className="row"><span className="nav-dl nav-dl-2" />정착 — 코어 잉크<span className="nav-dl-n">{dProficient}</span></div>
            <div className="row"><span className="nav-dl nav-dl-3" />개척 완료 — 금테<span className="nav-dl-n">{dMastered}</span></div>
          </div>
        </div>

        <a className="nav-guide" href="#guide">✎ 학습 길잡이에게 물어보기</a>
      </aside>
    </>
  );
}
