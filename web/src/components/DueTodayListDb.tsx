// DB-backed "오늘 풀어요" list. Refreshes on mount and every 60s.
// Falls back to "new" problems (never seen) once dues are exhausted so the
// queue stays non-empty until the student has seen every problem.
import { useEffect, useState } from 'react';

type Card = {
  slug: string; href: string; subject: string; number: number;
  unit: string | null; tier: string | null;
  state: string | null; nextReview: string | null; source: string;
};

const TIER_COLOR: Record<string, string> = {
  early: 'text-emerald-300',
  mid: 'text-amber-300',
  high: 'text-orange-300',
  killer: 'text-rose-300',
};

export default function DueTodayListDb() {
  const [due, setDue] = useState<Card[]>([]);
  const [neu, setNew] = useState<Card[]>([]);
  const [err, setErr] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  async function load() {
    try {
      const r = await fetch('/api/due-today?limit=20&includeNew=1', { cache: 'no-store' });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const j = await r.json();
      setDue(j.due ?? []);
      setNew(j.new ?? []);
      setErr(null);
    } catch (e) {
      setErr(String((e as Error).message ?? e));
    } finally { setLoading(false); }
  }
  useEffect(() => {
    load();
    const t = window.setInterval(load, 60_000);
    return () => window.clearInterval(t);
  }, []);

  if (loading) return <section className="card text-sm text-zinc-500">불러오는 중…</section>;
  if (err) return <section className="card text-sm text-rose-400">⚠ {err}</section>;

  const total = due.length + neu.length;

  return (
    <section className="card">
      <header className="flex items-center justify-between mb-3">
        <div>
          <h2 className="text-sm font-semibold">오늘 풀어요</h2>
          <p className="text-xs text-[color:var(--color-muted)]">
            복습 큐 {due.length}개 {neu.length > 0 && `· 신규 ${neu.length}개`}
          </p>
        </div>
        <span className="stat-num text-lg">{total}</span>
      </header>

      {total === 0 ? (
        <p className="text-sm text-[color:var(--color-subtle)] py-4 text-center">
          ✨ 오늘 풀 문제 없음. 신규 회차 인제스트하거나 mastery=mature 문제를 review로 돌리세요.
        </p>
      ) : (
        <ul className="space-y-1">
          {due.map((c) => (
            <li key={c.slug}>
              <a href={c.href} className="flex items-center justify-between gap-2 px-2 py-1.5 -mx-2 rounded hover:bg-zinc-800/60 transition">
                <span className="text-sm truncate">
                  <span className={`font-mono ${TIER_COLOR[c.tier ?? ''] ?? 'text-zinc-300'}`}>
                    [{c.tier ?? '?'}]
                  </span>
                  {' '}
                  <span className="text-zinc-200">{c.source} #{c.number}</span>
                  {c.unit && <span className="text-zinc-500 ml-2 text-xs">{c.unit}</span>}
                </span>
                <span className="text-[10px] text-zinc-500 whitespace-nowrap">{c.state ?? 'due'} · {c.nextReview ?? '?'}</span>
              </a>
            </li>
          ))}
          {neu.length > 0 && (
            <li className="pt-2 mt-2 border-t border-zinc-800">
              <p className="text-[10px] uppercase tracking-wide text-zinc-600 mb-1">신규 (never seen)</p>
            </li>
          )}
          {neu.map((c) => (
            <li key={c.slug}>
              <a href={c.href} className="flex items-center justify-between gap-2 px-2 py-1 -mx-2 rounded hover:bg-zinc-800/60 transition">
                <span className="text-sm truncate">
                  <span className={`font-mono ${TIER_COLOR[c.tier ?? ''] ?? 'text-zinc-300'}`}>
                    [{c.tier ?? '?'}]
                  </span>
                  {' '}
                  <span className="text-zinc-300">{c.source} #{c.number}</span>
                  {c.unit && <span className="text-zinc-500 ml-2 text-xs">{c.unit}</span>}
                </span>
                <span className="text-[10px] text-zinc-600 whitespace-nowrap">new</span>
              </a>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
