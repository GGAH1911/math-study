// 오답 상세의 우측 서랍 내용 — 본문 섬과 **같은 요청**을 공유한다(`content-entry` 캐시).
import { useContentEntry } from '../lib/content-entry.ts';

type FM = { error_type?: string; revisit_date?: string; next_review?: string; lesson?: string; problem?: string };

// 'docs/problems/<slug>.md' (flat) → 경로형 slug 'YYYY/round/<slug>'
const SUBJECT_RE = /^(\d{4})_(.+)_(?:공통|기하|미적분|확률과통계|단일)_\d+$/;
const fmtProblemPath = (p: string) => {
  const flat = p.replace(/^docs\/problems\//, '').replace(/\.md$/, '');
  const m = flat.match(SUBJECT_RE);
  return m ? `${m[1]}/${m[2]}/${flat}` : flat;
};
const labelOf = (s: string) => s.split('/').pop() ?? s;
// ★방출물의 날짜는 **문자열**이다(SSR 은 Date 객체라 toISOString 을 불렀다).
const day = (d?: string) => (d ? String(d).slice(0, 10) : null);

export default function MistakeMeta({ id }: { id: string }) {
  const s = useContentEntry<FM>('mistakes', id);
  if (s.status !== 'ready') return null;
  const fm = s.entry.data;
  return (
    <>
      <section className="card">
        <h3 className="text-xs uppercase tracking-[0.15em] text-[color:var(--color-subtle)] mb-2">오답 정보</h3>
        <dl className="text-sm space-y-1.5">
          <div className="flex justify-between">
            <dt className="text-[color:var(--color-muted)]">오류 유형</dt>
            <dd><span className={`chip chip-error-${fm.error_type}`}>{fm.error_type}</span></dd>
          </div>
          {day(fm.revisit_date) && (
            <div className="flex justify-between">
              <dt className="text-[color:var(--color-muted)]">다시 풀 날</dt><dd>{day(fm.revisit_date)}</dd>
            </div>
          )}
          {day(fm.next_review) && (
            <div className="flex justify-between">
              <dt className="text-[color:var(--color-muted)]">다음 복습</dt><dd>{day(fm.next_review)}</dd>
            </div>
          )}
        </dl>
        {fm.lesson && <p className="text-xs text-[color:var(--color-muted)] mt-3 leading-relaxed">{fm.lesson}</p>}
      </section>

      {fm.problem && (
        <section className="card">
          <h3 className="text-xs uppercase tracking-[0.15em] text-[color:var(--color-subtle)] mb-2">원 문제</h3>
          <a className="text-sm text-[color:var(--color-accent)] hover:underline"
             href={`/problems/${fmtProblemPath(fm.problem)}`}>
            {labelOf(fmtProblemPath(fm.problem))} →
          </a>
        </section>
      )}
    </>
  );
}
