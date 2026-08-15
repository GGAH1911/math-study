import { useEffect, useRef, useState } from 'react';

type ChipOption = { key: string; label: string; count: number };
type Axis = { name: string; label: string; attr: string; items: ChipOption[] };

type Props = {
  axes: Axis[];
  total: number;
  // 회차별 렌즈는 중간 그룹(.problem-group)이 있어 카드→그룹→섹션 3단으로 접는다.
  // 단원별 렌즈는 그룹이 없어 omit → 카드→섹션 2단.
  groupSelector?: string;
  // 단원별 렌즈: concepts 탭과 동일한 과목→단원 2단 collapse 를 켠다(.pdomain-toggle/.punit-toggle 위임 + 필터 시 자동 펼침).
  collapsible?: boolean;
};

function readQuerySet(name: string): Set<string> | null {
  if (typeof window === 'undefined') return null;
  const p = new URLSearchParams(window.location.search).get(name);
  if (p == null) return null;
  if (!p) return new Set();
  return new Set(p.split(',').map((s) => s.trim()).filter(Boolean));
}

function writeQuerySet(name: string, set: Set<string>) {
  if (typeof window === 'undefined') return;
  const url = new URL(window.location.href);
  // opt-in: 빈 Set = 전체(필터 없음) → param 삭제. 선택된 게 있으면 그것만 기록.
  if (set.size === 0) url.searchParams.delete(name);
  else url.searchParams.set(name, [...set].join(','));
  window.history.replaceState(null, '', url.toString());
}

export default function ProblemFilters({ axes, total, groupSelector, collapsible = false }: Props) {
  // opt-in: 빈 Set = 그 축 전체(필터 없음). 클릭으로 좁힌다.
  // (SSR/CSR 첫 렌더 모두 빈 Set → hydration mismatch 없음.)
  const [sets, setSets] = useState<Record<string, Set<string>>>(
    () => Object.fromEntries(axes.map((a) => [a.name, new Set<string>()])),
  );
  const [search, setSearch] = useState('');
  const [debounced, setDebounced] = useState('');
  const [hydrated, setHydrated] = useState(false);
  const [visibleCount, setVisibleCount] = useState(total);
  // 과목→단원 collapse 상태(단원별 렌즈 전용). concepts 탭과 동일 전략.
  const [expandedDomains, setExpandedDomains] = useState<Set<string>>(() => new Set());
  const [expandedUnits, setExpandedUnits] = useState<Set<string>>(() => new Set());
  const [allDomainIds, setAllDomainIds] = useState<string[]>([]);
  const searchRef = useRef<HTMLInputElement | null>(null);
  // 목록이 클라이언트에서 다시 그려졌음을 알리는 카운터(아래 problems:rendered 참조).
  const [renderTick, setRenderTick] = useState(0);

  // 마운트 후 URL 상태 replay. document 완료 전엔 카드가 아직 스트리밍 중이라
  // (2584장) querySelectorAll 이 놓치므로 readyState==='complete' 까지 첫 패스 보류.
  useEffect(() => {
    setSets((prev) => {
      const next = { ...prev };
      for (const a of axes) {
        const s = readQuerySet(a.name);
        if (s) next[a.name] = s;
      }
      return next;
    });
    const q = new URLSearchParams(window.location.search).get('q') ?? '';
    if (q) { setSearch(q); setDebounced(q.trim().toLowerCase()); }
    if (document.readyState === 'complete') setHydrated(true);
    else {
      const onLoad = () => setHydrated(true);
      window.addEventListener('load', onLoad, { once: true });
      return () => window.removeEventListener('load', onLoad);
    }
  }, []);

  useEffect(() => {
    const t = setTimeout(() => setDebounced(search.trim().toLowerCase()), 200);
    return () => clearTimeout(t);
  }, [search]);

  // ★Phase 3: 목록이 **클라이언트에서** 그려지면 카드가 `readyState==='complete'` **이후**에
  //   생긴다. 위 hydrated 가드는 SSR 스트리밍만 기다리므로, 그대로 두면 첫 필터 패스가
  //   빈 DOM 을 훑고 끝나 **필터가 죽는다**(카드는 보이는데 검색·칩이 아무 반응 없음).
  //   목록 섬이 다 그린 뒤 `problems:rendered` 를 쏘면 여기서 다시 훑는다.
  useEffect(() => {
    const onRendered = () => setRenderTick((n) => n + 1);
    window.addEventListener('problems:rendered', onRendered);
    return () => window.removeEventListener('problems:rendered', onRendered);
  }, []);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      const tag = (e.target as HTMLElement | null)?.tagName;
      if (tag === 'INPUT' || tag === 'TEXTAREA') {
        if (e.key === 'Escape') (e.target as HTMLElement).blur();
        return;
      }
      if (e.key === '/') {
        searchRef.current?.focus();
        searchRef.current?.select();
        e.preventDefault();
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, []);

  // DOM 필터: .problem-card-wrap 에 .filtered-out 토글 → 빈 그룹/섹션도 접음.
  useEffect(() => {
    if (!hydrated) return;
    const wraps = document.querySelectorAll<HTMLElement>('.problem-card-wrap');
    let visible = 0;
    for (const el of wraps) {
      let pass = true;
      for (const a of axes) {
        const sel = sets[a.name];
        if (sel.size === 0) continue; // 빈 Set = 그 축 전체 통과 (opt-in)
        const v = el.dataset[a.attr] ?? '';
        // 빈 값은 그 축을 통과 (수능엔 grade, 일부엔 tier 없음).
        if (v && !sel.has(v)) { pass = false; break; }
      }
      if (pass && debounced) {
        const label = el.dataset.label ?? '';
        if (!label.includes(debounced)) pass = false;
      }
      el.classList.toggle('filtered-out', !pass);
      if (pass) visible++;
    }
    if (groupSelector) {
      for (const grp of document.querySelectorAll<HTMLElement>(groupSelector)) {
        const hasVisible = !!grp.querySelector('.problem-card-wrap:not(.filtered-out)');
        // 매칭 문제 없는 회차만 숨김. <details> 펼침/접힘은 사용자 설정 유지(자동 펼침 안 함).
        grp.classList.toggle('filtered-out', !hasVisible);
      }
    }
    for (const s of document.querySelectorAll<HTMLElement>('.problem-lens-section')) {
      s.classList.toggle('filtered-out', !s.querySelector('.problem-card-wrap:not(.filtered-out)'));
    }
    // 단원별 렌즈: 매칭 카드 없는 단원 그룹·과목 섹션도 접어 숨김.
    for (const grp of document.querySelectorAll<HTMLElement>('.problem-unit-group')) {
      grp.classList.toggle('filtered-out', !grp.querySelector('.problem-card-wrap:not(.filtered-out)'));
    }
    for (const sec of document.querySelectorAll<HTMLElement>('.problem-domain-section')) {
      sec.classList.toggle('filtered-out', !sec.querySelector('.problem-card-wrap:not(.filtered-out)'));
    }
    setVisibleCount(visible);
  }, [hydrated, sets, debounced, axes, groupSelector, renderTick]);

  // URL 동기화 (새로고침/북마크 복원). hydrated 가드로 마운트 replay 가 방금 읽은 param 을 즉시 지우지 않게.
  useEffect(() => {
    if (!hydrated) return;
    for (const a of axes) writeQuerySet(a.name, sets[a.name]);
  }, [hydrated, sets, axes]);
  useEffect(() => {
    if (!hydrated) return;
    const url = new URL(window.location.href);
    if (search.trim()) url.searchParams.set('q', search.trim());
    else url.searchParams.delete('q');
    window.history.replaceState(null, '', url.toString());
  }, [hydrated, search]);

  const toggle = (name: string, key: string) =>
    setSets((prev) => {
      const next = new Set(prev[name]);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return { ...prev, [name]: next };
    });
  // opt-in: "전체" = 빈 Set(필터 해제), anyFilter = 선택된 칩이 하나라도 있음.
  const setAxisAll = (name: string) =>
    setSets((prev) => ({ ...prev, [name]: new Set<string>() }));
  const isAll = (name: string) => sets[name].size === 0;
  const anyFilter = axes.some((a) => sets[a.name].size > 0) || !!debounced;
  const resetAll = () => {
    setSets(Object.fromEntries(axes.map((a) => [a.name, new Set<string>()])));
    setSearch('');
  };

  // ── 과목→단원 collapse (concepts 탭과 동일 전략) — collapsible 일 때만, 토글 위임 ──
  // 회차별 렌즈(collapsible=false)엔 .pdomain-toggle 이 없어 querySelectorAll 이 비어 no-op.
  useEffect(() => {
    if (!hydrated || !collapsible) return;
    const dBtns = Array.from(document.querySelectorAll<HTMLElement>('.pdomain-toggle'));
    setAllDomainIds(dBtns.map((b) => b.dataset.pdomain ?? '').filter(Boolean));
    const onDomain = (e: Event) => {
      const id = (e.currentTarget as HTMLElement).dataset.pdomain;
      if (!id) return;
      setExpandedDomains((prev) => {
        const next = new Set(prev);
        if (next.has(id)) next.delete(id); else next.add(id);
        return next;
      });
    };
    const uBtns = Array.from(document.querySelectorAll<HTMLElement>('.punit-toggle'));
    const onUnit = (e: Event) => {
      const id = (e.currentTarget as HTMLElement).dataset.punit;
      if (!id) return;
      setExpandedUnits((prev) => {
        const next = new Set(prev);
        if (next.has(id)) next.delete(id); else next.add(id);
        return next;
      });
    };
    dBtns.forEach((b) => b.addEventListener('click', onDomain));
    uBtns.forEach((b) => b.addEventListener('click', onUnit));
    return () => {
      dBtns.forEach((b) => b.removeEventListener('click', onDomain));
      uBtns.forEach((b) => b.removeEventListener('click', onUnit));
    };
  }, [hydrated, collapsible]);

  // 접힘 반영: 필터 active 면 전부 펼침(매칭 카드 보이게), 아니면 expanded 집합 외 접힘.
  useEffect(() => {
    if (!hydrated || !collapsible) return;
    const force = anyFilter;
    for (const body of document.querySelectorAll<HTMLElement>('.pdomain-body')) {
      const id = body.dataset.pdomainBody ?? '';
      body.classList.toggle('collapsed', !(force || expandedDomains.has(id)));
    }
    for (const btn of document.querySelectorAll<HTMLElement>('.pdomain-toggle')) {
      const id = btn.dataset.pdomain ?? '';
      const open = force || expandedDomains.has(id);
      const chev = btn.querySelector('.pdomain-chevron');
      if (chev) chev.textContent = open ? '▾' : '▸';
      btn.setAttribute('aria-expanded', String(open));
    }
    for (const ul of document.querySelectorAll<HTMLElement>('.punit-problems')) {
      const id = ul.dataset.punitProblems ?? '';
      ul.classList.toggle('collapsed', !(force || expandedUnits.has(id)));
    }
    for (const btn of document.querySelectorAll<HTMLElement>('.punit-toggle')) {
      const id = btn.dataset.punit ?? '';
      const open = force || expandedUnits.has(id);
      btn.textContent = open ? '▾' : '▸';
      btn.setAttribute('aria-expanded', String(open));
    }
  }, [hydrated, collapsible, expandedDomains, expandedUnits, anyFilter]);

  const allDomainsExpanded = allDomainIds.length > 0 && allDomainIds.every((id) => expandedDomains.has(id));

  return (
    <div className="sticky top-0 z-20 -mx-6 px-6 py-3 bg-[color:var(--color-bg)]/95 backdrop-blur border-b border-[color:var(--color-border)] space-y-2">
      <div className="flex items-center gap-3 flex-wrap">
        <div className="relative flex-1 min-w-[200px] max-w-md">
          <input
            ref={searchRef}
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="문제 검색 — 회차·단원·출제의도 (/ 단축키)"
            className="w-full bg-[color:var(--color-surface)] border border-[color:var(--color-border)] rounded-md px-3 py-1.5 text-sm placeholder:text-[color:var(--color-subtle)] focus:outline-none focus:border-[color:var(--color-accent)]"
          />
          {search && (
            <button
              type="button"
              onClick={() => setSearch('')}
              className="absolute right-2 top-1/2 -translate-y-1/2 text-[color:var(--color-subtle)] hover:text-[color:var(--color-text)] text-xs"
              aria-label="검색어 지우기"
            >×</button>
          )}
        </div>
        <span className="text-xs text-[color:var(--color-muted)] tabular-nums">
          {visibleCount}/{total}
          {anyFilter && (
            <button
              type="button"
              onClick={resetAll}
              className="ml-3 text-[color:var(--color-accent)] hover:underline"
            >모두 해제</button>
          )}
        </span>
        {collapsible && allDomainIds.length > 0 && (
          <button
            type="button"
            onClick={() => setExpandedDomains(allDomainsExpanded ? new Set() : new Set(allDomainIds))}
            disabled={anyFilter}
            className="ml-auto chip opacity-70 hover:opacity-100 disabled:opacity-30 disabled:cursor-not-allowed"
            title={anyFilter ? '필터 중에는 매칭 문제가 모두 보입니다' : allDomainsExpanded ? '모든 과목 접기' : '모든 과목 펼치기'}
          >
            {allDomainsExpanded ? '◢ 모두 접기' : '◣ 모두 펼치기'}
          </button>
        )}
      </div>

      {axes.map((a) => (
        <FilterRow
          key={a.name}
          label={a.label}
          items={a.items}
          selected={sets[a.name]}
          onToggle={(k) => toggle(a.name, k)}
          onAll={() => setAxisAll(a.name)}
          allActive={isAll(a.name)}
        />
      ))}
    </div>
  );
}

function FilterRow({
  label, items, selected, onToggle, onAll, allActive,
}: {
  label: string;
  items: ChipOption[];
  selected: Set<string>;
  onToggle: (k: string) => void;
  onAll: () => void;
  allActive: boolean;
}) {
  if (items.length === 0) return null;
  return (
    <div className="flex items-center gap-2 text-xs flex-wrap">
      <span className="text-[10px] uppercase tracking-[0.15em] text-[color:var(--color-subtle)] min-w-[3.5rem]">
        {label}
      </span>
      <button
        type="button"
        onClick={onAll}
        className={`chip ${allActive ? 'border-[color:var(--color-text)]/40' : 'opacity-50'} hover:opacity-100`}
        title="전체로"
      >
        {allActive ? '● 전체' : '○ 전체로'}
      </button>
      {items.map((o) => {
        const on = selected.has(o.key);
        return (
          <button
            key={o.key}
            type="button"
            onClick={() => onToggle(o.key)}
            className={`chip ${on ? '' : 'opacity-40'} hover:opacity-100 inline-flex items-center gap-1.5`}
          >
            <span>{o.label}</span>
            <span className="tabular-nums opacity-70 text-[10px]">{o.count}</span>
          </button>
        );
      })}
    </div>
  );
}
