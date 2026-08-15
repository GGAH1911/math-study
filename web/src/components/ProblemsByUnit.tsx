// 기출 — 단원별 목록. Phase 3 전환 6호. 데이터는 `/api/content-index/problems`.
//
// ★단원→과목 매핑은 방출기가 `concept-graph.json` 에서 만들어 목록에 **맵 하나로** 얹어 준다
//   (`unitDomain`). 문항마다 domain 을 넣으면 4,210번 반복돼 목록이 그만큼 커진다.
//
// ★필터가 죽지 않게 `problems:rendered` 를 쏜다 — `ProblemFilters` 는 `readyState==='complete'`
//   까지 기다렸다 DOM 을 훑는데 클라이언트 렌더는 그 이후에 카드가 생긴다(problems/index 와 동일).
import { useEffect, useMemo, useState } from 'react';
import { groupByUnit, buildFilterAxes, cardProps, dataAttrs } from '../lib/problem-card';
import { DOMAIN_ORDER, DOMAIN_COLOR } from '../lib/concept-meta';
import ProblemFilters from './ProblemFilters.tsx';
import ProblemCard from './ProblemCard.tsx';

type Row = { id: string; [k: string]: unknown };
type State =
  | { status: 'loading' }
  | { status: 'error'; message: string }
  | { status: 'ready'; entries: Row[]; unitDomain: Record<string, string> };

export default function ProblemsByUnit() {
  const [s, setS] = useState<State>({ status: 'loading' });

  useEffect(() => {
    let alive = true;
    fetch('/api/content-index/problems', { headers: { accept: 'application/json' } })
      .then(async (r) => {
        if (!r.ok) {
          const b = await r.json().catch(() => ({} as { error?: string; hint?: string }));
          throw new Error(b.hint ? `${b.error} — ${b.hint}` : `HTTP ${r.status}`);
        }
        return r.json() as Promise<{ entries?: Row[]; unitDomain?: Record<string, string> }>;
      })
      .then((d) => { if (alive) setS({ status: 'ready', entries: d.entries ?? [], unitDomain: d.unitDomain ?? {} }); })
      .catch((e: unknown) => { if (alive) setS({ status: 'error', message: e instanceof Error ? e.message : String(e) }); });
    return () => { alive = false; };
  }, []);

  const shaped = useMemo(
    () => (s.status === 'ready' ? s.entries.map((e) => ({ id: e.id, data: e })) : []),
    [s],
  );
  const unitGroups = useMemo(() => (shaped.length ? groupByUnit(shaped as never) : []), [shaped]);
  const axes = useMemo(() => (shaped.length ? buildFilterAxes(shaped as never) : []), [shaped]);

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

  // 단원 그룹 → 과목별 묶음. 순서는 concepts 탭과 같은 DOMAIN_ORDER.
  const domainOf = (unit: string) => s.unitDomain[unit.normalize('NFC')] ?? '기타';
  const byDomain = new Map<string, typeof unitGroups>();
  for (const g of unitGroups) {
    const d = g.unit === '기타' ? '기타' : domainOf(g.unit);
    if (!byDomain.has(d)) byDomain.set(d, []);
    byDomain.get(d)!.push(g);
  }
  const orderedDomains = [
    ...DOMAIN_ORDER.filter((d) => byDomain.has(d)),
    ...[...byDomain.keys()].filter((d) => !(DOMAIN_ORDER as readonly string[]).includes(d)),
  ];

  return (
    <>
      <ProblemFilters axes={axes} total={s.entries.length} collapsible />
      {orderedDomains.map((domain) => {
        const units = byDomain.get(domain)!;
        const problemCount = units.reduce((a, g) => a + g.problems.length, 0);
        return (
          <section className="problem-domain-section space-y-2" data-pdomain-section={domain} key={domain}>
            <button
              type="button"
              className="pdomain-toggle w-full flex items-center gap-3 sticky top-16 bg-[color:var(--color-bg)]/85 backdrop-blur py-2 -mx-6 px-6 z-10 border-b border-[color:var(--color-border)] text-left hover:bg-[color:var(--color-surface)]/50 transition-colors"
              data-pdomain={domain}
              aria-expanded="false"
            >
              <span className="pdomain-chevron text-[color:var(--color-subtle)] text-xs w-3 shrink-0 select-none">▸</span>
              <h2 className="text-base font-semibold flex items-center gap-2">
                <span className="size-2.5 rounded-full inline-block" style={{ background: DOMAIN_COLOR[domain] ?? '#71717a' }} />
                {domain}
              </h2>
              <span className="text-xs text-[color:var(--color-muted)]">{units.length}단원 · {problemCount}문제</span>
            </button>

            <div className="pdomain-body collapsed space-y-2" data-pdomain-body={domain}>
              {units.map((g) => (
                <div className="problem-unit-group" data-punit-group={g.unit} key={g.unit}>
                  <div className="flex items-center gap-2 py-1">
                    <button
                      type="button"
                      className="punit-toggle shrink-0 size-6 rounded-md border border-[color:var(--color-border)] text-[color:var(--color-subtle)] hover:text-[color:var(--color-text)] hover:border-[color:var(--color-border-strong)] grid place-items-center text-xs select-none"
                      data-punit={g.unit}
                      aria-expanded="false"
                      aria-label={`${g.problems.length}개 문제 펼치기`}
                    >▸</button>
                    <h3 className="text-sm font-medium">
                      {g.unit.replace(/_/g, ' ')}
                      <span className="ml-1.5 text-xs text-[color:var(--color-muted)] font-normal">{g.problems.length}문항</span>
                    </h3>
                  </div>
                  <ul className="punit-problems collapsed grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3 ml-8"
                      data-punit-problems={g.unit}>
                    {g.problems.map((p) => (
                      <li className="problem-card-wrap" key={p.id} {...dataAttrs(p)}>
                        <ProblemCard {...cardProps(p)} />
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </section>
        );
      })}
    </>
  );
}
