// `RoundDetails.astro` 의 React 판 — Phase 3 에서 기출 목록이 클라이언트로 옮겨가며 필요해졌다.
// ⚠️ 마크업·클래스는 `.astro` 판과 1:1 이다. 한쪽만 고치면 화면이 페이지마다 달라 보인다.
//    3단계가 끝나 `.astro` 소비처가 없어지면 그쪽을 지운다.
import { roundTitle, TIER_BADGE } from '../lib/problem-meta';
import { cardProps, dataAttrs, subjectBreakdown, type RoundGroup } from '../lib/problem-card';

export default function RoundDetails({ round: r }: { round: RoundGroup }) {
  return (
    <details className="problem-group rounded-lg border border-[color:var(--color-border)]">
      <summary className="flex items-center justify-between gap-3 px-3 py-2 cursor-pointer list-none rounded-lg hover:bg-[color:var(--color-surface-2)]/40">
        <span className="flex items-center gap-2 min-w-0">
          <span className="round-marker text-[color:var(--color-subtle)] text-xs select-none transition-transform">▸</span>
          <span className="font-medium text-sm truncate min-w-0">{roundTitle(r.meta)}</span>
          {/* 유형 breakdown 은 모바일에서 숨긴다 — 회차(연도)가 중요하지 종류는 안 중요(사장님). */}
          <span className="hidden sm:inline truncate text-[11px] text-[color:var(--color-subtle)]">{subjectBreakdown(r.problems)}</span>
        </span>
        <a
          href={`/exam/round/${r.year}/${r.round}`}
          onClick={(e) => e.stopPropagation()}
          className="chip text-[11px] hover:border-[color:var(--color-accent)] shrink-0"
        >▶ 시험 모드</a>
      </summary>
      <ul className="px-2 pb-2 pt-1 divide-y divide-[color:var(--color-border)]/30">
        {r.problems.map((p) => {
          const cp = cardProps(p);
          const unit = String(p.data.unit ?? '').trim().replace(/_/g, ' ');
          const badge = cp.tier ? TIER_BADGE[cp.tier] : null;
          return (
            <li key={p.id} className="problem-card-wrap" {...dataAttrs(p)}>
              <a href={cp.href} className="flex items-center gap-3 py-1.5 px-2 text-sm rounded hover:bg-[color:var(--color-surface-2)]/50">
                <span className="w-20 shrink-0 font-medium tabular-nums">{cp.title}</span>
                <span className="flex-1 min-w-0 truncate text-[color:var(--color-subtle)]">{unit || '—'}</span>
                {badge && <span className={`chip text-[10px] shrink-0 ${badge.cls}`}>{badge.text}</span>}
                {cp.score != null && cp.score !== '' && (
                  <span className="text-[11px] text-[color:var(--color-subtle)] tabular-nums shrink-0">{cp.score}점</span>
                )}
                {cp.solved && <span className="text-emerald-400 text-xs shrink-0" title="해결">✓</span>}
              </a>
            </li>
          );
        })}
      </ul>
    </details>
  );
}
