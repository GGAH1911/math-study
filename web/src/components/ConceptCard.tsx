// `ConceptCard.astro` 의 React 판 — Phase 3 목록 페이지들이 아일랜드 안에서 쓴다.
//
// ★왜 두 벌인가: Astro 컴포넌트는 아일랜드(React) 안에서 못 쓴다. 목록을 클라이언트로 옮기면
//   카드도 React 여야 한다. 서버 렌더가 남아 있는 페이지는 `.astro` 판을 계속 쓴다.
//   ⚠️ **두 벌이 갈라지면 화면이 페이지마다 달라 보인다.** 마크업·클래스는 `.astro` 판과
//   1:1 로 맞춰 뒀다 — 한쪽을 고치면 다른 쪽도 고칠 것. 3단계가 끝나면 `.astro` 판을 지운다.
//
// ★수식은 **같은 SSOT** 를 쓴다(`renderMathSegments` + katex). 요약에 `$...$` 가 들어 있고,
//   여기만 다른 정규화를 쓰면 같은 노트가 목록과 본문에서 다르게 보인다.
import katex from 'katex';
import { renderMathSegments } from '../lib/katex-normalize.mjs';

export type Chip = { label: string; class?: string };
export type Meta = { key: string; value: string };

export type ConceptCardProps = {
  href: string;
  title: string;
  subtitle?: string;
  chips?: Chip[];
  meta?: Meta[];
  description?: string;
  emphasized?: boolean;
};

export default function ConceptCard({
  href, title, subtitle, chips = [], meta = [], description, emphasized = false,
}: ConceptCardProps) {
  // 요약은 우리가 만든 마크다운에서 온다(사용자 입력이 아니다). `.astro` 판과 동일한 경로다.
  const descHtml = description ? renderMathSegments(description, katex) : '';
  return (
    <article className={`concept-card card relative${emphasized ? ' concept-card-unit' : ''}`}>
      <a href={href} className="block">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0 flex-1">
            <h3 className={`font-semibold leading-snug ${emphasized ? 'text-lg' : 'text-base'}`}>{title}</h3>
            {subtitle && (
              <p className="text-[10px] font-mono text-[color:var(--color-subtle)] mt-0.5 truncate">{subtitle}</p>
            )}
          </div>
          <div className="flex flex-wrap gap-1 justify-end shrink-0">
            {chips.map((c, i) => <span key={i} className={`chip ${c.class ?? ''}`}>{c.label}</span>)}
          </div>
        </div>
        {description && (
          <p className="text-sm text-[color:var(--color-muted)] mt-2 line-clamp-2"
             dangerouslySetInnerHTML={{ __html: descHtml }} />
        )}
        {meta.length > 0 && (
          <dl className="mt-3 grid grid-cols-2 gap-x-3 gap-y-1 text-[11px] text-[color:var(--color-subtle)]">
            {meta.map((m, i) => (
              <div key={i} className="flex justify-between gap-2">
                <dt className="uppercase tracking-wider">{m.key}</dt>
                <dd className="text-[color:var(--color-muted)] truncate text-right">{m.value}</dd>
              </div>
            ))}
          </dl>
        )}
      </a>
    </article>
  );
}
