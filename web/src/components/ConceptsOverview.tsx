// 개념 대시보드 — Phase 3 전환 8호(B그룹 마지막). 데이터는 `/api/concepts-overview`.
//
// ★서버가 **완성된 트리**를 준다. 이 컴포넌트는 계산하지 않고 그리기만 한다 —
//   단원↔스포크 매칭이 파일 경로 의미(NFC 정규화 포함)에 기대는 로직이라 브라우저로 옮기면
//   같은 규칙이 두 벌 생긴다.
// ★필터가 죽지 않게 `concepts:rendered` 를 쏜다(ProblemFilters 와 같은 함정).
import { useEffect, useState } from 'react';
import ConceptCard, { type ConceptCardProps } from './ConceptCard.tsx';
import ConceptFilters from './ConceptFilters.tsx';

type Attrs = Record<string, string>;
type Node = { card: ConceptCardProps & { graphHref?: string; practice?: unknown; progress?: unknown }; attrs: Attrs };
type Group = { unitId: string | null; unit: Node | null; spokes: Node[] };
type Domain = { domain: string; label: string; color: string; nodeCount: number; unitCount: number; groups: Group[] };
type RecUnit = { unitId: string; label: string; grade?: string; domain?: string; progressPercent: number; status: string };
type Overview = {
  total: number; interactiveCount: number;
  byType: Record<string, number>;
  filterOptions: unknown; tracks: unknown;
  recRows: Array<{ icon: string; label: string; units: RecUnit[] }>;
  domains: Domain[];
};

export default function ConceptsOverview() {
  const [d, setD] = useState<Overview | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    fetch('/api/concepts-overview', { headers: { accept: 'application/json' } })
      .then(async (r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json() as Promise<Overview>;
      })
      .then((v) => { if (alive) setD(v); })
      .catch((e: unknown) => { if (alive) setError(e instanceof Error ? e.message : String(e)); });
    return () => { alive = false; };
  }, []);

  useEffect(() => { if (d) window.dispatchEvent(new Event('concepts:rendered')); }, [d]);

  if (error) {
    return (
      <div className="card text-sm">
        <p className="font-semibold">개념 목록을 불러오지 못했습니다.</p>
        <p className="text-xs text-[color:var(--color-muted)] mt-1 break-all">{error}</p>
      </div>
    );
  }
  if (!d) return <p className="text-sm text-[color:var(--color-muted)] py-12 text-center">불러오는 중…</p>;
  if (d.total === 0) return <p className="text-sm text-[color:var(--color-muted)] py-12 text-center">아직 개념이 없습니다.</p>;

  return (
    <>
      <p className="text-sm text-[color:var(--color-muted)]">
        {d.total}개 노드 · 단원 {d.byType.unit} / 정의 {d.byType.definition} / 정리 {d.byType.theorem} / 예제 {d.byType.example}
      </p>

      <ConceptFilters
        options={d.filterOptions as never}
        tracks={d.tracks as never}
        totalConcepts={d.total}
        interactiveCount={d.interactiveCount}
      />

      {d.recRows.length > 0 && (
        <div className="space-y-3">
          {d.recRows.map((row) => (
            <section className="space-y-1.5" key={row.label}>
              <h3 className="text-xs font-semibold text-[color:var(--color-muted)]">
                {row.icon} {row.label} <span className="text-[color:var(--color-subtle)] tabular-nums">{row.units.length}</span>
              </h3>
              <div className="flex gap-2 overflow-x-auto pb-1">
                {row.units.map((u) => (
                  <a key={u.unitId} href={`/concepts/${u.unitId}`}
                     className="shrink-0 w-44 card p-2.5 hover:border-[color:var(--color-accent)] transition">
                    <div className="text-sm font-medium truncate">{u.label}</div>
                    <div className="text-[10px] text-[color:var(--color-subtle)] truncate">{u.grade ?? ''} · {u.domain ?? ''}</div>
                    <div className="mt-1.5 h-1.5 rounded-full bg-[color:var(--color-surface-2)] overflow-hidden">
                      <div className="h-full rounded-full"
                           style={{ width: `${Math.max(2, u.progressPercent)}%`, background: `var(--color-mastery-${u.status})` }} />
                    </div>
                  </a>
                ))}
              </div>
            </section>
          ))}
        </div>
      )}

      {d.domains.map((dom) => (
        <section className="concept-domain-section space-y-3" data-domain-section={dom.domain} key={dom.domain}>
          <button
            type="button"
            className="domain-toggle w-full flex items-center gap-3 sticky top-16 bg-[color:var(--color-bg)]/85 backdrop-blur py-2 -mx-6 px-6 z-10 border-b border-[color:var(--color-border)] text-left hover:bg-[color:var(--color-surface)]/50 transition-colors"
            data-domain={dom.domain}
            aria-expanded="false"
          >
            <span className="domain-chevron text-[color:var(--color-subtle)] text-xs w-3 shrink-0 select-none">▸</span>
            <h2 className="text-base font-semibold flex items-center gap-2">
              <span className="size-2.5 rounded-full inline-block" style={{ background: dom.color }} />
              {dom.label}
            </h2>
            <span className="text-xs text-[color:var(--color-muted)]">
              {dom.nodeCount}개 노드 ({dom.unitCount} 단원)
            </span>
          </button>

          <div className="concept-domain-body collapsed space-y-3" data-domain-body={dom.domain}>
            {dom.groups.map((g) => (
              <div className="concept-unit-group space-y-2" data-unit-group={g.unitId ?? 'orphan'} key={g.unitId ?? 'orphan'}>
                {g.unit && (
                  <div className="flex items-stretch gap-2">
                    {g.spokes.length > 0 && (
                      <button
                        type="button"
                        className="unit-toggle shrink-0 w-7 rounded-md border border-[color:var(--color-border)] text-[color:var(--color-subtle)] hover:text-[color:var(--color-text)] hover:border-[color:var(--color-border-strong)] grid place-items-center text-xs select-none"
                        data-unit={g.unitId ?? undefined}
                        aria-expanded="false"
                        aria-label={`${g.spokes.length}개 하위 개념 펼치기`}
                        title={`${g.spokes.length}개 하위 개념`}
                      >▸</button>
                    )}
                    <div className="concept-card-wrap flex-1 min-w-0" {...g.unit.attrs}>
                      <ConceptCard {...g.unit.card} />
                    </div>
                  </div>
                )}
                {g.spokes.length > 0 && (
                  <ul
                    className={`concept-spokes grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3${
                      g.unit ? ' collapsed ml-0 md:ml-9 border-l-2 border-[color:var(--color-border)]/40 pl-3 md:pl-4' : ''}`}
                    data-unit-spokes={g.unitId ?? 'orphan'}
                  >
                    {g.spokes.map((c) => (
                      <li className="concept-card-wrap" key={c.card.href} {...c.attrs}>
                        <ConceptCard {...c.card} />
                      </li>
                    ))}
                  </ul>
                )}
                {!g.unit && g.spokes.length > 0 && (
                  <p className="text-[11px] text-[color:var(--color-subtle)] -mt-1">기타 (단원 미연결)</p>
                )}
              </div>
            ))}
          </div>
        </section>
      ))}
    </>
  );
}
