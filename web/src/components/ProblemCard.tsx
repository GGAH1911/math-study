// 문제 카드(썸네일) — `ProblemCard.astro` 의 React 판. `problems/units` 가 유일한 소비처다.
//
// ★스타일은 여기 없다. `.astro` 판은 컴포넌트 스코프 `<style>` 을 가졌지만 React 아일랜드는
//   그걸 못 쓴다. `problems/units.astro` 의 `<style is:global>` 로 옮겼다 — 클래스 이름은 동일.
//   ⚠️ 클래스를 바꾸려면 **양쪽을 같이** 고쳐야 한다.
import { TIER_BADGE, FORMAT_LABEL } from '../lib/problem-meta';

export type ProblemCardProps = {
  href: string;
  thumb: string;
  title: string;
  tier?: string | null;
  format?: string | null;
  score?: string | number | null;
  cognitive?: string | null;
  solved?: boolean;
};

export default function ProblemCard({
  href, thumb, title, tier, format, score, cognitive, solved = false,
}: ProblemCardProps) {
  const badge = tier ? TIER_BADGE[tier] : null;
  return (
    <a href={href} className="problem-card block overflow-hidden">
      <div className="thumb-wrap">
        <img src={thumb} alt={title} loading="lazy" decoding="async" className="thumb" />
        {solved && (
          <span className="absolute top-1.5 left-1.5 text-[10px] px-1.5 py-0.5 rounded-full bg-emerald-500/25 text-emerald-200 border border-emerald-500/40">✓</span>
        )}
      </div>
      <div className="p-2.5 space-y-1">
        <div className="flex items-center justify-between gap-2">
          <h3 className="text-sm font-semibold truncate">{title}</h3>
          {badge && (
            <span className={`text-[10px] px-1.5 py-0.5 rounded-full border shrink-0 ${badge.cls}`}>{badge.text}</span>
          )}
        </div>
        <div className="flex items-center gap-1.5 text-[10px] text-[color:var(--color-subtle)]">
          {format && <span>{FORMAT_LABEL[format] ?? format}</span>}
          {score && <span>· {score}점</span>}
          {cognitive && <span>· {cognitive}</span>}
        </div>
      </div>
    </a>
  );
}
