// `RoundNav.astro` 의 React 판 — 상세 페이지가 섬으로 옮겨가며 필요해졌다.
// ★API 는 `{id, subject, number}` 로 평탄화해 준다(엔트리 전체를 보낼 이유가 없다).
export type NavItem = { id: string; subject: string; number: number };

export default function RoundNav({ prev, nexts, curSubject, currentLabel }: {
  prev: NavItem | null; nexts: NavItem[]; curSubject?: string; currentLabel: string;
}) {
  if (!prev && nexts.length === 0) return null;
  const btn = 'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm border border-[color:var(--color-border)] bg-[color:var(--color-surface-2)] hover:border-[color:var(--color-accent)] transition whitespace-nowrap';
  const off = 'px-3 py-1.5 text-sm text-[color:var(--color-subtle)] opacity-40 select-none whitespace-nowrap';
  // 과목 경계를 넘을 때(예: 선택 첫문제→공통)만 과목명 접두.
  const pfx = (e: NavItem) => (e.subject && e.subject !== curSubject ? `${e.subject} ` : '');

  return (
    <nav className="flex items-center justify-between gap-2 flex-wrap" aria-label="회차 내 문제 이동">
      {prev
        ? <a href={`/problems/${prev.id}`} className={btn} rel="prev"><span aria-hidden="true">←</span> {pfx(prev)}{prev.number}번</a>
        : <span className={off}><span aria-hidden="true">←</span> 이전</span>}
      <span className="text-xs text-[color:var(--color-muted)] truncate px-1">{currentLabel}</span>
      {nexts.length === 0
        ? <span className={off}>다음 <span aria-hidden="true">→</span></span>
        : nexts.length === 1
          ? <a href={`/problems/${nexts[0].id}`} className={btn} rel="next">{pfx(nexts[0])}{nexts[0].number}번 <span aria-hidden="true">→</span></a>
          : <span className="flex flex-wrap gap-1.5 justify-end">
              {nexts.map((n) => <a key={n.id} href={`/problems/${n.id}`} className={btn}>{n.subject} {n.number}번 <span aria-hidden="true">→</span></a>)}
            </span>}
    </nav>
  );
}
