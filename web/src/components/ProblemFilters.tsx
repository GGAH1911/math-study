import { useEffect, useRef, useState } from 'react';

type ChipOption = { key: string; label: string; count: number };
type Axis = { name: string; label: string; attr: string; items: ChipOption[] };

type Props = {
  axes: Axis[];
  total: number;
  // 회차별 렌즈는 중간 그룹(.problem-group)이 있어 카드→그룹→섹션 3단으로 접는다.
  // 단원별 렌즈는 그룹이 없어 omit → 카드→섹션 2단.
  groupSelector?: string;
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

export default function ProblemFilters({ axes, total, groupSelector }: Props) {
  // opt-in: 빈 Set = 그 축 전체(필터 없음). 클릭으로 좁힌다.
  // (SSR/CSR 첫 렌더 모두 빈 Set → hydration mismatch 없음.)
  const [sets, setSets] = useState<Record<string, Set<string>>>(
    () => Object.fromEntries(axes.map((a) => [a.name, new Set<string>()])),
  );
  const [search, setSearch] = useState('');
  const [debounced, setDebounced] = useState('');
  const [hydrated, setHydrated] = useState(false);
  const [visibleCount, setVisibleCount] = useState(total);
  const searchRef = useRef<HTMLInputElement | null>(null);

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
        grp.classList.toggle('filtered-out', !grp.querySelector('.problem-card-wrap:not(.filtered-out)'));
      }
    }
    for (const s of document.querySelectorAll<HTMLElement>('.problem-lens-section')) {
      s.classList.toggle('filtered-out', !s.querySelector('.problem-card-wrap:not(.filtered-out)'));
    }
    setVisibleCount(visible);
  }, [hydrated, sets, debounced, axes, groupSelector]);

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
