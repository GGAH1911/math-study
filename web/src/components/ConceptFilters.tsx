import { useEffect, useMemo, useRef, useState } from 'react';

type ChipOption = { key: string; label: string; count: number; color?: string };

type Props = {
  options: {
    masteries: ChipOption[];
    domains: ChipOption[];
    grades: ChipOption[];
  };
  tracks?: { key: string; grades: string[] }[];
  totalConcepts: number;
  interactiveCount?: number;
};

function readQuerySet(name: string): Set<string> | null {
  if (typeof window === 'undefined') return null;
  const p = new URLSearchParams(window.location.search).get(name);
  if (p == null) return null;
  if (!p) return new Set();
  return new Set(p.split(',').map((s) => s.trim()).filter(Boolean));
}

function writeQuerySet(name: string, set: Set<string>, allKeys: string[]) {
  if (typeof window === 'undefined') return;
  const url = new URL(window.location.href);
  // Treat "all selected" as "no filter" → drop the query param to keep URLs clean.
  // opt-in: 빈 Set = 전체(필터 없음) → param 삭제.
  if (set.size === 0) {
    url.searchParams.delete(name);
  } else {
    url.searchParams.set(name, [...set].join(','));
  }
  window.history.replaceState(null, '', url.toString());
}

export default function ConceptFilters({ options, tracks = [], totalConcepts, interactiveCount = 0 }: Props) {
  const masteryKeys = useMemo(() => options.masteries.map((o) => o.key), [options.masteries]);
  const domainKeys = useMemo(() => options.domains.map((o) => o.key), [options.domains]);
  const gradeKeys = useMemo(() => options.grades.map((o) => o.key), [options.grades]);

  // Start every filter as "all selected" so the SSR and the client's first
  // render agree (no hydration mismatch). The URL is read in a mount effect
  // below — for `?mastery=learning` the state then narrows to that subset.
  // opt-in: 빈 Set = 전체(필터 없음). 클릭으로 좁힌다. (SSR/CSR 모두 빈 Set)
  const [mastery, setMastery] = useState<Set<string>>(() => new Set());
  const [domain, setDomain] = useState<Set<string>>(() => new Set());
  const [grade, setGrade] = useState<Set<string>>(() => new Set());
  const [search, setSearch] = useState<string>('');
  const [debounced, setDebounced] = useState('');
  const [interactiveOnly, setInteractiveOnly] = useState(false);
  const [hydrated, setHydrated] = useState(false);
  const [visibleCount, setVisibleCount] = useState<number>(totalConcepts);
  const [expandedUnits, setExpandedUnits] = useState<Set<string>>(() => new Set());
  const [expandedDomains, setExpandedDomains] = useState<Set<string>>(() => new Set());
  const [allDomainIds, setAllDomainIds] = useState<string[]>([]);
  const searchRef = useRef<HTMLInputElement | null>(null);

  // After hydration, replay any URL state. `hydrated` guards the
  // write-back effects so they don't immediately strip the URL params
  // while we're still loading them in.
  //
  // We also defer setting `hydrated` until the document is fully parsed —
  // the filter island sits near the top of the page and React hydrates it
  // as soon as it's reached, but the ~2789 concept cards stream in below
  // it. If we apply filters before the DOM is complete, querySelectorAll
  // misses cards that haven't been parsed yet and the page renders in a
  // half-filtered state.
  useEffect(() => {
    const m = readQuerySet('mastery');
    if (m) setMastery(m);
    const d = readQuerySet('domain');
    if (d) setDomain(d);
    const g = readQuerySet('grade');
    if (g) setGrade(g);
    const q = new URLSearchParams(window.location.search).get('q') ?? '';
    if (q) { setSearch(q); setDebounced(q.trim().toLowerCase()); }
    if (new URLSearchParams(window.location.search).get('interactive') === '1') setInteractiveOnly(true);
    if (document.readyState === 'complete') {
      setHydrated(true);
    } else {
      const onLoad = () => setHydrated(true);
      window.addEventListener('load', onLoad, { once: true });
      return () => window.removeEventListener('load', onLoad);
    }
  }, []);

  // Debounce search input so we don't re-query on every keystroke.
  useEffect(() => {
    const t = setTimeout(() => setDebounced(search.trim().toLowerCase()), 200);
    return () => clearTimeout(t);
  }, [search]);

  // `/` focuses the search box, `Esc` blurs it (unless typing in another field).
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

  // Apply filters to the static DOM: toggle a `.filtered-out` class on each
  // card wrapper, then on unit-groups and domain sections that end up empty.
  // Runs only AFTER the URL-replay mount effect has set the real initial
  // filter state — otherwise we'd briefly mark everything visible (with
  // the all-selected default), then have to redo the work, which on a
  // 2789-card page leaves the DOM in a half-toggled state.
  useEffect(() => {
    if (!hydrated) return;
    const wraps = document.querySelectorAll<HTMLElement>('.concept-card-wrap');
    let visible = 0;
    for (const el of wraps) {
      const m = el.dataset.mastery ?? '';
      const d = el.dataset.domain ?? '';
      const g = el.dataset.grade ?? '';
      const label = el.dataset.label ?? '';
      const id = el.dataset.id ?? '';
      const unit = el.dataset.unit ?? '';
      const passMastery = mastery.size === 0 || mastery.has(m);
      const passDomain = domain.size === 0 || domain.has(d);
      const passGrade = grade.size === 0 || !g || grade.has(g);
      const passSearch =
        !debounced ||
        label.includes(debounced) ||
        id.includes(debounced) ||
        unit.includes(debounced);
      const passInteractive = !interactiveOnly || el.dataset.interactive === '1';
      const visibleHere = passMastery && passDomain && passGrade && passSearch && passInteractive;
      el.classList.toggle('filtered-out', !visibleHere);
      if (visibleHere) visible++;
    }
    const groups = document.querySelectorAll<HTMLElement>('.concept-unit-group');
    for (const grp of groups) {
      const anyVisible = grp.querySelector('.concept-card-wrap:not(.filtered-out)');
      grp.classList.toggle('filtered-out', !anyVisible);
    }
    const sections = document.querySelectorAll<HTMLElement>('.concept-domain-section');
    for (const s of sections) {
      const anyVisible = s.querySelector('.concept-unit-group:not(.filtered-out)');
      s.classList.toggle('filtered-out', !anyVisible);
    }
    setVisibleCount(visible);
  }, [hydrated, mastery, domain, grade, debounced, interactiveOnly]);

  // Sync each filter set back to the URL so refresh / bookmarks restore state.
  // Guarded by `hydrated` so the mount-time URL replay doesn't immediately
  // erase the params it just loaded.
  useEffect(() => {
    if (!hydrated) return;
    writeQuerySet('mastery', mastery, masteryKeys);
  }, [hydrated, mastery, masteryKeys]);
  useEffect(() => {
    if (!hydrated) return;
    writeQuerySet('domain', domain, domainKeys);
  }, [hydrated, domain, domainKeys]);
  useEffect(() => {
    if (!hydrated) return;
    writeQuerySet('grade', grade, gradeKeys);
  }, [hydrated, grade, gradeKeys]);
  useEffect(() => {
    if (!hydrated) return;
    const url = new URL(window.location.href);
    if (search.trim()) url.searchParams.set('q', search.trim());
    else url.searchParams.delete('q');
    window.history.replaceState(null, '', url.toString());
  }, [hydrated, search]);
  useEffect(() => {
    if (!hydrated) return;
    const url = new URL(window.location.href);
    if (interactiveOnly) url.searchParams.set('interactive', '1');
    else url.searchParams.delete('interactive');
    window.history.replaceState(null, '', url.toString());
  }, [hydrated, interactiveOnly]);

  const toggle = (set: Set<string>, setter: (s: Set<string>) => void, key: string) => {
    const next = new Set(set);
    if (next.has(key)) next.delete(key);
    else next.add(key);
    setter(next);
  };
  // opt-in: "전체" = 빈 Set(필터 해제).
  const setAll = (setter: (s: Set<string>) => void, _all: string[]) => setter(new Set());

  const masteryAll = mastery.size === 0;
  const domainAll = domain.size === 0;
  const gradeAll = grade.size === 0;
  const anyFilter = !masteryAll || !domainAll || !gradeAll || !!debounced || interactiveOnly;

  const resetAll = () => {
    setMastery(new Set());
    setDomain(new Set());
    setGrade(new Set());
    setSearch('');
    setInteractiveOnly(false);
  };

  // --- 단원 접기/펼치기 --------------------------------------------------
  // 토글 버튼에 listener 부착 + 전체 단원 id 수집 (문서 완성 후, 카드가 다 파싱된 뒤).
  useEffect(() => {
    if (!hydrated) return;
    const btns = Array.from(document.querySelectorAll<HTMLElement>('.unit-toggle'));
    const onClick = (e: Event) => {
      const id = (e.currentTarget as HTMLElement).dataset.unit;
      if (!id) return;
      setExpandedUnits((prev) => {
        const next = new Set(prev);
        if (next.has(id)) next.delete(id); else next.add(id);
        return next;
      });
    };
    btns.forEach((b) => b.addEventListener('click', onClick));
    return () => btns.forEach((b) => b.removeEventListener('click', onClick));
  }, [hydrated]);

  // 접힘 반영: 필터 active 면 전부 펼침(필터가 가시성 결정), 아니면 expandedUnits 외 접힘.
  useEffect(() => {
    if (!hydrated) return;
    const force = anyFilter;
    for (const ul of document.querySelectorAll<HTMLElement>('.concept-spokes')) {
      const id = ul.dataset.unitSpokes ?? '';
      if (id === 'orphan') continue;
      ul.classList.toggle('collapsed', !(force || expandedUnits.has(id)));
    }
    for (const btn of document.querySelectorAll<HTMLElement>('.unit-toggle')) {
      const id = btn.dataset.unit ?? '';
      const open = force || expandedUnits.has(id);
      btn.textContent = open ? '▾' : '▸';
      btn.setAttribute('aria-expanded', String(open));
    }
  }, [hydrated, expandedUnits, anyFilter]);

  // --- 도메인(과목) 접기/펼치기 -------------------------------------------
  // 최상위 레벨. 기본 전부 접힘 → 클릭하면 그 과목의 단원 목록이 펼쳐지고,
  // 단원은 다시 개별 토글로 스포크를 편다(과목 → 단원 → 스포크 계층 접기).
  useEffect(() => {
    if (!hydrated) return;
    const btns = Array.from(document.querySelectorAll<HTMLElement>('.domain-toggle'));
    setAllDomainIds(btns.map((b) => b.dataset.domain ?? '').filter(Boolean));
    const onClick = (e: Event) => {
      const id = (e.currentTarget as HTMLElement).dataset.domain;
      if (!id) return;
      setExpandedDomains((prev) => {
        const next = new Set(prev);
        if (next.has(id)) next.delete(id); else next.add(id);
        return next;
      });
    };
    btns.forEach((b) => b.addEventListener('click', onClick));
    return () => btns.forEach((b) => b.removeEventListener('click', onClick));
  }, [hydrated]);

  // 도메인 접힘 반영: 필터 active 면 전부 펼침(필터가 가시성 결정), 아니면 expandedDomains 외 접힘.
  useEffect(() => {
    if (!hydrated) return;
    const force = anyFilter;
    for (const body of document.querySelectorAll<HTMLElement>('.concept-domain-body')) {
      const id = body.dataset.domainBody ?? '';
      body.classList.toggle('collapsed', !(force || expandedDomains.has(id)));
    }
    for (const btn of document.querySelectorAll<HTMLElement>('.domain-toggle')) {
      const id = btn.dataset.domain ?? '';
      const open = force || expandedDomains.has(id);
      const chev = btn.querySelector('.domain-chevron');
      if (chev) chev.textContent = open ? '▾' : '▸';
      btn.setAttribute('aria-expanded', String(open));
    }
  }, [hydrated, expandedDomains, anyFilter]);

  const allExpanded = allDomainIds.length > 0 && allDomainIds.every((id) => expandedDomains.has(id));
  const applyTrack = (grades: string[]) => setGrade(new Set(grades.filter((g) => gradeKeys.includes(g))));

  return (
    <div className="sticky top-0 z-20 -mx-6 px-6 py-3 bg-[color:var(--color-bg)]/95 backdrop-blur border-b border-[color:var(--color-border)] space-y-2">
      <div className="flex items-center gap-3 flex-wrap">
        <div className="relative flex-1 min-w-[200px] max-w-md">
          <input
            ref={searchRef}
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="개념 이름 검색 (/ 단축키)"
            className="w-full bg-[color:var(--color-surface)] border border-[color:var(--color-border)] rounded-md px-3 py-1.5 text-sm placeholder:text-[color:var(--color-subtle)] focus:outline-none focus:border-[color:var(--color-primary,#3b82f6)]"
          />
          {search && (
            <button
              type="button"
              onClick={() => setSearch('')}
              className="absolute right-2 top-1/2 -translate-y-1/2 text-[color:var(--color-subtle)] hover:text-[color:var(--color-fg)] text-xs"
              aria-label="검색어 지우기"
            >×</button>
          )}
        </div>
        <span className="text-xs text-[color:var(--color-muted)] tabular-nums">
          {visibleCount}/{totalConcepts}
          {anyFilter && (
            <button
              type="button"
              onClick={resetAll}
              className="ml-3 text-[color:var(--color-primary,#3b82f6)] hover:underline"
            >모두 해제</button>
          )}
        </span>
        <button
          type="button"
          onClick={() => setInteractiveOnly((v) => !v)}
          aria-pressed={interactiveOnly}
          className={`chip chip-interactive ${interactiveOnly ? '' : 'opacity-50'} hover:opacity-100`}
          title="인터랙티브 위젯 있는 개념만 보기"
        >🔭 인터랙티브{interactiveCount ? ` ${interactiveCount}` : ''}</button>
        {allDomainIds.length > 0 && (
          <button
            type="button"
            onClick={() => setExpandedDomains(allExpanded ? new Set() : new Set(allDomainIds))}
            disabled={anyFilter}
            className="ml-auto chip opacity-70 hover:opacity-100 disabled:opacity-30 disabled:cursor-not-allowed"
            title={anyFilter ? '필터 중에는 매칭 항목이 모두 보입니다' : allExpanded ? '모든 과목 접기' : '모든 과목 펼치기'}
          >
            {allExpanded ? '◢ 모두 접기' : '◣ 모두 펼치기'}
          </button>
        )}
      </div>

      <FilterRow
        label="마스터리"
        items={options.masteries}
        selected={mastery}
        onToggle={(k) => toggle(mastery, setMastery, k)}
        onAll={() => setAll(setMastery, masteryKeys)}
        allActive={masteryAll}
        chipClass={(o) => `chip-mastery-${o.key}`}
      />
      <FilterRow
        label="도메인"
        items={options.domains}
        selected={domain}
        onToggle={(k) => toggle(domain, setDomain, k)}
        onAll={() => setAll(setDomain, domainKeys)}
        allActive={domainAll}
        dotColor={(o) => o.color}
      />
      <FilterRow
        label="학년"
        items={options.grades}
        selected={grade}
        onToggle={(k) => toggle(grade, setGrade, k)}
        onAll={() => setAll(setGrade, gradeKeys)}
        allActive={gradeAll}
      />
      {tracks.length > 0 && (
        <div className="flex items-center gap-2 text-xs flex-wrap">
          <span className="text-[10px] uppercase tracking-[0.15em] text-[color:var(--color-subtle)] min-w-[3.5rem]">
            트랙
          </span>
          {tracks.map((t) => (
            <button
              key={t.key}
              type="button"
              onClick={() => applyTrack(t.grades)}
              className="chip opacity-70 hover:opacity-100"
              title={`${t.grades.join(' · ')} 단원만 보기`}
            >{t.key}</button>
          ))}
          <button
            type="button"
            onClick={() => setAll(setGrade, gradeKeys)}
            className="chip opacity-50 hover:opacity-100"
            title="모든 학년"
          >전체</button>
        </div>
      )}
    </div>
  );
}

function FilterRow({
  label, items, selected, onToggle, onAll, allActive, chipClass, dotColor,
}: {
  label: string;
  items: ChipOption[];
  selected: Set<string>;
  onToggle: (k: string) => void;
  onAll: () => void;
  allActive: boolean;
  chipClass?: (o: ChipOption) => string;
  dotColor?: (o: ChipOption) => string | undefined;
}) {
  return (
    <div className="flex items-center gap-2 text-xs flex-wrap">
      <span className="text-[10px] uppercase tracking-[0.15em] text-[color:var(--color-subtle)] min-w-[3.5rem]">
        {label}
      </span>
      <button
        type="button"
        onClick={onAll}
        className={`chip ${allActive ? 'border-[color:var(--color-fg)]/40' : 'opacity-50'} hover:opacity-100`}
        title="전체로"
      >
        {allActive ? '● 전체' : '○ 전체로'}
      </button>
      {items.map((o) => {
        const on = selected.has(o.key);
        const cls = chipClass?.(o) ?? '';
        const color = dotColor?.(o);
        return (
          <button
            key={o.key}
            type="button"
            onClick={() => onToggle(o.key)}
            className={`chip ${cls} ${on ? '' : 'opacity-40'} hover:opacity-100 inline-flex items-center gap-1.5`}
          >
            {color && (
              <span className="size-2 rounded-full inline-block" style={{ background: color }} />
            )}
            <span>{o.label}</span>
            <span className="tabular-nums opacity-70 text-[10px]">{o.count}</span>
          </button>
        );
      })}
    </div>
  );
}
