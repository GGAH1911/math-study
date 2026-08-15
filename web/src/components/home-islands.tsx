// 홈 대시보드 섬들 — 프론트매터가 먹이던 네 군데를 각각 맡는다.
//
// ★네 섬이 **같은 요청**을 쓴다(`useJsonOnce('/api/home')`). 홈에서 마크업이 흩어져 있어
//   한 섬으로 못 묶는데, 각자 fetch 하면 요청이 네 번 나간다.
// ★`HealthCards`·`ActivityFeed`·`TutorChat` 은 **자기 데이터를 스스로 읽는 Astro 컴포넌트**라
//   페이지에 그대로 둔다(프론트매터가 먹이지 않는다). 앱 전환 시 별도 항목이다.
import { useJsonOnce } from '../lib/content-entry.ts';
import PaperHero from './PaperHero.tsx';
import ConceptDAG from './ConceptDAG.tsx';
import MasteryDonut from './MasteryDonut.tsx';
import { MathishText } from '../lib/mathish';

type Home = {
  dateLine: string; suggestion: string; dueCount: number;
  todayConcept: { id: string; label: string; unit: string | null; domain: string | null; hasWidget: boolean } | null;
  todaySpec: unknown; todayBlurb: string;
  graphForUser: { stats?: { nodes?: number } };
  units: { started: number; total: number };
  us: { unknown: number; learning: number; proficient: number; mastered: number };
  recentSyntheses: Array<{ slug: string; title: string; created: string | null; origin_concept: string | null; excerpt: string | null }>;
  totalSyntheses: number;
  leaf: Record<string, string>;
};

const useHome = () => useJsonOnce<Home>('/api/home');

/** 히어로 — 날짜줄·삽화·오늘의 개념·권장 작업·버튼. */
export function HomeHero() {
  const s = useHome();
  if (s.status !== 'ready') {
    return <div className="min-h-[260px]" aria-hidden />;  // 높이를 잡아 둔다(늦게 들어오며 화면이 튀지 않게)
  }
  const d = s.data;
  return (
    <>
      <p className="font-hand text-[22px] leading-none text-[color:var(--color-muted)]">{d.dateLine}</p>
      <h1 className="mt-2 text-3xl md:text-4xl font-bold tracking-tight">오늘의 페이지</h1>
      <div className="relative">
        <PaperHero spec={d.todaySpec as never} label={d.todayConcept?.label ?? ''} />
      </div>
      {d.todayConcept && (
        <div className="mt-3 max-w-3xl">
          <p className="text-sm text-[color:var(--color-muted)]">
            <span className="font-hand text-[16px] sm:text-[18px] text-[color:var(--color-subtle)] mr-1.5">오늘의 개념</span>
            <a href={`/concepts/${d.todayConcept.id}`} className="font-medium text-[color:var(--color-text)] hover:text-[color:var(--color-accent)] hover:underline">「{d.todayConcept.label}」</a>
            {d.todayConcept.hasWidget && <span className="iw-mark" title="인터랙티브 위젯 있음"> 🔭</span>}
            {(d.todayConcept.unit || d.todayConcept.domain) && (
              <span className="text-[color:var(--color-subtle)]"> · {[d.todayConcept.domain, d.todayConcept.unit].filter(Boolean).join(' · ')}</span>
            )}
          </p>
          <p className="mt-1 text-sm leading-relaxed text-[color:var(--color-text)]">
            {d.todayBlurb && <span>{d.todayBlurb} </span>}
            <a href={`/concepts/${d.todayConcept.id}`} className="text-[color:var(--color-accent)] hover:underline font-medium whitespace-nowrap">→ 알아보기</a>
          </p>
        </div>
      )}
      <div className="mt-4 flex flex-wrap items-end justify-between gap-4">
        <p className="text-sm text-[color:var(--color-muted)] max-w-2xl">
          <span className="text-[color:var(--color-subtle)]">권장 다음 작업:</span> {d.suggestion}
        </p>
        <div className="flex flex-wrap items-center gap-2 w-full sm:w-auto">
          <a href="#due-today" className="btn-ink whitespace-nowrap">
            {d.dueCount > 0 ? `이어서 풀기 — 복습 ${d.dueCount}건` : '오늘의 풀이 큐 열기'}
          </a>
          <a href="/graph" className="btn-ghost whitespace-nowrap">◈ 개념 지도 열기</a>
        </div>
      </div>
    </>
  );
}

/** 개념 지도 미리보기(데스크탑 전용 — 페이지가 `hidden lg:block` 으로 감싼다). */
export function HomeGraph() {
  const s = useHome();
  if (s.status !== 'ready') return <p className="text-sm text-[color:var(--color-muted)] p-6">불러오는 중…</p>;
  if (!s.data.graphForUser.stats?.nodes) {
    return <p className="text-sm text-[color:var(--color-muted)] p-6">아직 concept 노드가 없습니다. <code className="text-[color:var(--color-accent)]">docs/concepts/</code>에 첫 페이지를 시드해보세요.</p>;
  }
  return <ConceptDAG data={s.data.graphForUser as never} variant="mini" />;
}

/** 단원 진행 — 도넛 + 범례. */
export function HomeProgress() {
  const s = useHome();
  if (s.status !== 'ready') return <p className="text-sm text-[color:var(--color-muted)]">불러오는 중…</p>;
  const { units, us } = s.data;
  const row = (key: keyof typeof us, label: string) => (
    <li className="flex items-center gap-2" key={key}>
      <span className={`size-2 rounded-full bg-[color:var(--color-mastery-${key})]`} />
      <span className="text-[color:var(--color-muted)]">{label}</span>
      <span className="ml-auto stat-num">{us[key]}</span>
    </li>
  );
  return (
    <>
      <header className="mb-3">
        <h2 className="text-sm font-semibold">단원 진행</h2>
        <p className="text-xs text-[color:var(--color-muted)]">
          착수 <span className="stat-num text-[color:var(--color-text)]">{units.started}</span> / {units.total} 단원 · 스포크 mastery 롤업
        </p>
      </header>
      <MasteryDonut unknown={us.unknown} learning={us.learning} proficient={us.proficient} mastered={us.mastered} />
      <ul className="mt-4 space-y-1.5 text-sm">
        {row('unknown', '미착수')}{row('learning', '학습중')}{row('proficient', '능숙')}{row('mastered', '마스터')}
      </ul>
    </>
  );
}

/** 최근 학습 노트 — 헤더 + 목록. 요약의 `$...$` 는 `MathishText` 가 렌더한다. */
export function HomeSyntheses() {
  const s = useHome();
  if (s.status !== 'ready') return <p className="text-sm text-[color:var(--color-muted)] py-3">불러오는 중…</p>;
  const { recentSyntheses: list, totalSyntheses, leaf } = s.data;
  return (
    <>
      <header className="mb-3 flex items-center justify-between">
        <div>
          <h2 className="text-sm font-semibold">🗒 최근 학습 노트</h2>
          <p className="text-xs text-[color:var(--color-muted)]">{totalSyntheses}개 · 채팅에서 저장한 영구 노트</p>
        </div>
        <a href="/syntheses" className="text-xs text-[color:var(--color-accent)] hover:underline">전체 보기 →</a>
      </header>
      {list.length === 0 ? (
        <p className="font-hand text-[18px] text-[color:var(--color-muted)] py-3">
          아직 저장한 노트가 없어요. 컨셉 페이지에서 LLM과 대화한 뒤
          <span className="text-[color:var(--color-fg)]"> "📝 학습 노트 작성 요청" → "💾 저장"</span> 으로 만들 수 있습니다.
        </p>
      ) : (
        <ul className="divide-y divide-[color:var(--color-border)]/40">
          {list.map((n) => (
            <li className="py-2 first:pt-0 last:pb-0" key={n.slug}>
              <div className="flex items-baseline gap-2">
                <a className="text-sm font-medium font-serif text-[color:var(--color-fg)] hover:text-[color:var(--color-accent)] truncate"
                   href={`/syntheses/${encodeURIComponent(n.slug)}`}>{n.title}</a>
                {n.created && <span className="text-[10px] text-[color:var(--color-subtle)] tabular-nums whitespace-nowrap">{n.created}</span>}
              </div>
              {n.origin_concept && (
                <a className="text-[11px] text-[color:var(--color-muted)] hover:text-[color:var(--color-accent)] truncate block"
                   href={`/concepts/${n.origin_concept}`} title={n.origin_concept}>← {leaf[n.slug]}</a>
              )}
              {n.excerpt && (
                <p className="text-xs text-[color:var(--color-muted)] mt-0.5 line-clamp-1">
                  <MathishText text={n.excerpt} display={false} />
                </p>
              )}
            </li>
          ))}
        </ul>
      )}
    </>
  );
}

/** 모바일 전용 개념 지도 진입점의 노드 수. */
export function HomeNodeCount() {
  const s = useHome();
  return <>{s.status === 'ready' ? (s.data.graphForUser.stats?.nodes ?? 0) : '…'}</>;
}
