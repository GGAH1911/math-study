// 기출 — 회차별 목록. Phase 3 전환 4호. 데이터는 `/api/content-index/problems`(방출물).
//
// ★필터(`ProblemFilters`)와 **같은 섬**에 둔다. 따로 두면 필터가 마운트 시 빈 DOM 을 훑고 끝나
//   죽는다. 여기서 목록을 그린 뒤 `problems:rendered` 를 쏘면 필터가 다시 훑는다.
//
// ★`groupByRound`·`buildFilterAxes` 는 `lib/problem-card` 것을 **그대로** 쓴다. 정렬·그룹핑
//   규칙을 여기서 다시 짜면 SSR 판과 갈라진다. 그 함수들은 `{id, data}` 모양을 기대하므로
//   방출물 항목(필드가 최상위)을 그 모양으로 감싸 준다.
import { useEffect, useMemo } from 'react';
import { useContentIndex, type Entry } from '../lib/content-index.ts';
import { groupByRound, buildFilterAxes, type RoundGroup } from '../lib/problem-card';
import ProblemFilters from './ProblemFilters.tsx';
import RoundDetails from './RoundDetails.tsx';

const h2cls = 'text-lg font-semibold border-b border-[color:var(--color-border)] pb-1.5';
const hint = 'text-xs font-normal text-[color:var(--color-subtle)] ml-1.5';

export default function ProblemsByRound() {
  const s = useContentIndex<Entry>('problems');

  // 방출물 항목 → 컬렉션 엔트리 모양. lib 함수들이 `.data.X` 를 읽는다.
  const shaped = useMemo(
    () => (s.status === 'ready' ? s.entries.map((e) => ({ id: e.id, data: e })) : []),
    [s],
  );
  const groups = useMemo(() => (shaped.length ? groupByRound(shaped as never) : new Map()), [shaped]);
  const axes = useMemo(() => (shaped.length ? buildFilterAxes(shaped as never) : []), [shaped]);

  // 목록이 DOM 에 올라간 뒤 필터에게 다시 훑으라고 알린다(위 설명 참조).
  useEffect(() => {
    if (shaped.length) window.dispatchEvent(new Event('problems:rendered'));
  }, [shaped]);

  if (s.status === 'loading') {
    return <p className="text-sm text-[color:var(--color-muted)] py-12 text-center">불러오는 중…</p>;
  }
  if (s.status === 'error') {
    return (
      <div className="card text-sm">
        <p className="font-semibold">기출 목록을 불러오지 못했습니다.</p>
        <p className="text-xs text-[color:var(--color-muted)] mt-1 break-all">{s.message}</p>
      </div>
    );
  }
  if (s.entries.length === 0) {
    return <p className="text-sm text-[color:var(--color-muted)] py-12 text-center">아직 문제가 없습니다.</p>;
  }

  // 시험종류 대분류 — SSR 판과 같은 로직(연도 desc 평탄화 후 종류별 버킷).
  const allRounds: RoundGroup[] = [...groups.values()].flat() as RoundGroup[];
  const ofType = (t: string) => allRounds.filter((r) => r.meta.exam_type === t);
  const isYeshi = (r: RoundGroup) => /예시/.test(r.meta.session ?? '');
  const suneung = ofType('수능').filter((r) => !isYeshi(r));
  const yeshi = ofType('수능').filter(isYeshi);
  const mopyeong = ofType('모의평가');
  const mock = ofType('모의고사');
  const mockByGrade = ['고3', '고2', '고1']
    .map((grade) => ({ grade, rounds: mock.filter((r) => r.meta.grade === grade) }))
    .filter((x) => x.rounds.length > 0);

  const section = (title: string, sub: string, rounds: RoundGroup[]) =>
    rounds.length > 0 && (
      <section className="problem-lens-section space-y-2" key={title}>
        <h2 className={h2cls}>{title}<span className={hint}>{sub}</span></h2>
        {rounds.map((r) => <RoundDetails key={`${r.year}/${r.round}`} round={r} />)}
      </section>
    );

  return (
    <>
      <ProblemFilters axes={axes} total={s.entries.length} groupSelector=".problem-group" />
      <div className="space-y-6">
        {section('수능', '대학수학능력시험', suneung)}
        {section('모의평가', '평가원 6월·9월', mopyeong)}
        {mockByGrade.map(({ grade, rounds }) => section(`${grade} 모의고사`, '교육청', rounds))}
        {section('예시문항', '평가원 예시', yeshi)}
      </div>
    </>
  );
}
