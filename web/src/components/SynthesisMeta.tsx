// 학습 노트 상세의 우측 서랍 — 본문 섬과 같은 요청을 공유한다.
//
// ★제목은 frontmatter 가 아니라 별도 빌드 산출물에서 온다(`derived.title`). 방출기가 개별
//   문서에도 실어 준다. 서버는 그 값을 모르므로 `<title>` 을 여기서 갱신한다.
import { useEffect } from 'react';
import { useContentEntry } from '../lib/content-entry.ts';
import { REVIEW_STATE_LABEL_KO } from '../lib/srs.ts';
import SynthesisDeleteButton from './SynthesisDeleteButton.tsx';

type FM = { created?: string; updated?: string; next_review?: string; review_state?: string;
            promoted_from?: string; origin_concept?: string };

const day = (d?: string) => (d ? String(d).slice(0, 10) : null);

export default function SynthesisMeta({ id }: { id: string }) {
  const s = useContentEntry<FM>('syntheses', id);
  const derived = s.status === 'ready' ? ((s.entry as { derived?: { title?: string; origin_title?: string } }).derived ?? {}) : {};

  const originSlug = s.status === 'ready'
    ? String(s.entry.data.origin_concept ?? '').replace(/^docs\/concepts\//, '').replace(/\.md$/, '')
    : '';
  const originLabel = originSlug.split('/').pop()?.replace(/_/g, ' ') ?? '';

  useEffect(() => {
    if (s.status !== 'ready') return;
    const title = derived.title ?? derived.origin_title ?? originLabel ?? id;
    document.title = `${title} · Math Study`;
  }, [s.status, derived.title, derived.origin_title, originLabel, id]);

  if (s.status !== 'ready') return null;
  const fm = s.entry.data;
  const created = day(fm.created) ?? id.match(/^(\d{4}-\d{2}-\d{2})/)?.[1] ?? null;

  return (
    <>
      <section className="card">
        <h3 className="text-xs uppercase tracking-[0.15em] text-[color:var(--color-subtle)] mb-2">메타정보</h3>
        <dl className="text-sm space-y-1.5">
          {created && <div className="flex justify-between"><dt className="text-[color:var(--color-muted)]">작성일</dt><dd>{created}</dd></div>}
          {day(fm.updated) && <div className="flex justify-between"><dt className="text-[color:var(--color-muted)]">수정일</dt><dd>{day(fm.updated)}</dd></div>}
          {fm.review_state && (
            <div className="flex justify-between"><dt className="text-[color:var(--color-muted)]">복습 상태</dt>
              <dd><span className="chip">{REVIEW_STATE_LABEL_KO[fm.review_state] ?? fm.review_state}</span></dd></div>
          )}
          {day(fm.next_review) && <div className="flex justify-between"><dt className="text-[color:var(--color-muted)]">다음 복습</dt><dd>{day(fm.next_review)}</dd></div>}
          {fm.promoted_from && <div className="flex justify-between"><dt className="text-[color:var(--color-muted)]">출처</dt><dd>{fm.promoted_from}</dd></div>}
        </dl>
      </section>

      {originSlug && (
        <section className="card">
          <h3 className="text-xs uppercase tracking-[0.15em] text-[color:var(--color-subtle)] mb-2">출처</h3>
          <a className="text-sm text-[color:var(--color-accent)] hover:underline block" href={`/concepts/${originSlug}`}>← {originLabel}</a>
          <p className="text-[10px] font-mono text-[color:var(--color-subtle)] mt-1 truncate" title={originSlug}>{originSlug}</p>
          <a href={`/graph?highlight=${encodeURIComponent(originSlug)}`}
             className="mt-3 block text-center px-3 py-1.5 rounded-md bg-indigo-500/10 hover:bg-indigo-500/20 border border-indigo-500/30 text-indigo-300 text-xs font-medium transition">
            개념 지도에서 보기 →
          </a>
        </section>
      )}

      <section className="card">
        <h3 className="text-xs uppercase tracking-[0.15em] text-[color:var(--color-subtle)] mb-2">목록</h3>
        <a className="text-sm text-[color:var(--color-accent)] hover:underline" href="/syntheses">← 학습 노트 전체</a>
      </section>

      <section className="card">
        <h3 className="text-xs uppercase tracking-[0.15em] text-[color:var(--color-subtle)] mb-2">관리</h3>
        <SynthesisDeleteButton slug={id} />
      </section>
    </>
  );
}
