import { useState, useMemo, useRef, useEffect } from 'react';

type Concept = { id: string; label: string; domain: string | null; grade: string | null; type: string };

// 목표 개념 검색 콤보박스 — 라벨/경로로 필터, 선택하면 /paths?goal=<id> 로 이동.
// 2838개 개념을 native datalist 로 넣으면 무겁고 한글 라벨 매칭이 들쭉날쭉해서 직접 구현.
export default function PathPicker({ concepts }: { concepts: Concept[] }) {
  const [q, setQ] = useState('');
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(0);
  const boxRef = useRef<HTMLDivElement | null>(null);

  const results = useMemo(() => {
    const s = q.trim().toLowerCase();
    if (!s) return [];
    const hit = concepts.filter(
      (c) => c.label.toLowerCase().includes(s) || c.id.toLowerCase().includes(s),
    );
    // 단원 먼저, 그다음 라벨 prefix 매칭 우선.
    hit.sort((a, b) => {
      const ua = a.type === 'unit' ? 0 : 1;
      const ub = b.type === 'unit' ? 0 : 1;
      if (ua !== ub) return ua - ub;
      const pa = a.label.toLowerCase().startsWith(s) ? 0 : 1;
      const pb = b.label.toLowerCase().startsWith(s) ? 0 : 1;
      if (pa !== pb) return pa - pb;
      return a.label.localeCompare(b.label, 'ko-KR');
    });
    return hit.slice(0, 25);
  }, [q, concepts]);

  useEffect(() => setActive(0), [q]);

  useEffect(() => {
    const onDoc = (e: MouseEvent) => {
      if (boxRef.current && !boxRef.current.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener('mousedown', onDoc);
    return () => document.removeEventListener('mousedown', onDoc);
  }, []);

  const go = (id: string) => {
    window.location.href = `/paths?goal=${encodeURIComponent(id)}`;
  };

  const onKey = (e: React.KeyboardEvent) => {
    if (!open || results.length === 0) return;
    if (e.key === 'ArrowDown') { e.preventDefault(); setActive((a) => Math.min(a + 1, results.length - 1)); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); setActive((a) => Math.max(a - 1, 0)); }
    else if (e.key === 'Enter') { e.preventDefault(); go(results[active].id); }
    else if (e.key === 'Escape') setOpen(false);
  };

  return (
    <div ref={boxRef} className="relative max-w-xl">
      <input
        type="text"
        value={q}
        onChange={(e) => { setQ(e.target.value); setOpen(true); }}
        onFocus={() => setOpen(true)}
        onKeyDown={onKey}
        placeholder="목표 개념·단원 검색 (예: 도함수의 활용, 삼각함수, 적분)"
        className="w-full bg-[color:var(--color-surface)] border border-[color:var(--color-border)] rounded-md px-3 py-2 text-sm placeholder:text-[color:var(--color-subtle)] focus:outline-none focus:border-[color:var(--color-accent)]"
      />
      {open && results.length > 0 && (
        <ul className="absolute z-30 mt-1 w-full max-h-80 overflow-y-auto rounded-md border border-[color:var(--color-border)] bg-[color:var(--color-surface)] shadow-lg">
          {results.map((c, i) => (
            <li key={c.id}>
              <button
                type="button"
                onMouseEnter={() => setActive(i)}
                onClick={() => go(c.id)}
                className={`w-full text-left px-3 py-1.5 flex items-center gap-2 ${i === active ? 'bg-[color:var(--color-bg)]' : ''}`}
              >
                <span className="text-sm truncate">{c.label}</span>
                {c.type === 'unit' && <span className="text-[10px] chip shrink-0">단원</span>}
                <span className="ml-auto text-[10px] text-[color:var(--color-subtle)] shrink-0">{c.grade ?? ''} · {c.domain ?? ''}</span>
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
