// 작업 로그 — Phase 3 C그룹. 데이터는 `/api/log`(어드민 전용).
import { useJsonOnce } from '../lib/content-entry.ts';

type Entry = { date: string; operation: string; subject: string };

const iconFor = (op: string): string => {
  if (op.startsWith('init')) return '✦';
  if (op.startsWith('smoke')) return '⌬';
  if (op.startsWith('ingest')) return '↧';
  if (op.startsWith('prune')) return '✂';
  if (op.startsWith('merge')) return '⇄';
  if (op.startsWith('env')) return '⚙';
  return '·';
};

export default function OpsLog() {
  const s = useJsonOnce<{ entries: Entry[] }>('/api/log');
  if (s.status === 'error') {
    return (
      <div className="card text-sm">
        <p className="font-semibold">로그를 불러오지 못했습니다.</p>
        <p className="text-xs text-[color:var(--color-muted)] mt-1 break-all">{s.message}</p>
      </div>
    );
  }
  if (s.status !== 'ready') return <p className="text-sm text-[color:var(--color-muted)] py-12 text-center">불러오는 중…</p>;

  const entries = s.data.entries;
  if (entries.length === 0) return <p className="text-sm text-[color:var(--color-muted)] py-12 text-center">로그가 비어 있습니다.</p>;

  const groups = new Map<string, Entry[]>();
  for (const e of entries) {
    if (!groups.has(e.date)) groups.set(e.date, []);
    groups.get(e.date)!.push(e);
  }

  return (
    <>
      <p className="text-sm text-[color:var(--color-muted)] -mt-4">{entries.length}개 엔트리 · docs/log.md (append-only)</p>
      {[...groups.entries()].map(([date, items]) => (
        <section className="space-y-3" key={date}>
          <h2 className="text-xs uppercase tracking-[0.18em] text-[color:var(--color-subtle)] sticky top-16 bg-[color:var(--color-bg)]/85 backdrop-blur py-2 -mx-6 px-6 z-10">{date}</h2>
          <ol className="space-y-2 ml-2 border-l border-[color:var(--color-border)]">
            {items.map((e, i) => (
              <li className="relative pl-6 pr-2 py-2" key={i}>
                <span className="absolute -left-3 top-3 inline-flex items-center justify-center size-6 rounded-full bg-[color:var(--color-surface)] border border-[color:var(--color-border)] text-xs text-[color:var(--color-accent)]">{iconFor(e.operation)}</span>
                <div className="text-sm font-medium">{e.operation}</div>
                <div className="text-xs text-[color:var(--color-muted)] mt-1 leading-relaxed">{e.subject}</div>
              </li>
            ))}
          </ol>
        </section>
      ))}
    </>
  );
}
