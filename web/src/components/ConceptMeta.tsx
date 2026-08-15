// 개념 상세 — 우측 서랍 섬. 본문 섬과 **같은 요청**을 쓴다(loadJsonOnce 캐시).
import { useEffect, useState } from 'react';
import { useConceptDetail, PREVIEW, type Group } from '../lib/concept-detail-shared.ts';
import LearningNoteButton from './LearningNoteButton.tsx';
import RegenerateBodyButton from './RegenerateBodyButton.tsx';

export default function ConceptMeta({ slug }: { slug: string }) {
  const s = useConceptDetail(slug);
  const [mastery, setMastery] = useState<string | null>(null);

  // PromotionCard 가 mastery 를 적용하면 리로드 없이 칩만 갱신한다.
  // (리로드는 대화의 promote 펜스 재프롬프트 루프를 유발해 제거된 적이 있다.)
  useEffect(() => {
    const KO: Record<string, string> = { unknown: '미습득', learning: '학습중', proficient: '능숙', mastered: '마스터' };
    const on = (e: Event) => {
      const det = (e as CustomEvent<{ slug: string; to: string }>).detail;
      if (det?.slug === slug) setMastery(KO[det.to] ?? det.to);
    };
    window.addEventListener('math-study:mastery-applied', on);
    return () => window.removeEventListener('math-study:mastery-applied', on);
  }, [slug]);

  if (s.status !== 'ready') return null;
  const d = s.data;
  const fm = d.data;
  const wid = (x: string) => !!d.hasWidgetOf[x];
  const linkList = (g: Group[], arrow: string) => (
    <div className="space-y-3 text-sm">
      {g.map((grp) => (
        <div key={grp.label}>
          <div className="text-[10px] uppercase tracking-wider text-[color:var(--color-muted)] mb-1">{grp.label}</div>
          <ul className="space-y-1 pl-1">
            {grp.items.map((it) => (
              <li key={it.slug}>
                <a className="text-[color:var(--color-accent)] hover:underline" href={`/concepts/${it.slug}`}>
                  {arrow} {it.label}{wid(it.slug) && <span className="iw-mark" title="인터랙티브 위젯 있음"> 🔭</span>}
                </a>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );

  return (
    <>
      {d.prereqGroups.length > 0 && (
        <section className="card">
          <h3 className="text-xs uppercase tracking-[0.15em] text-[color:var(--color-subtle)] mb-2">선수 개념</h3>
          {linkList(d.prereqGroups, '←')}
        </section>
      )}
      {d.enablesGroups.length > 0 && (
        <section className="card">
          <h3 className="text-xs uppercase tracking-[0.15em] text-[color:var(--color-subtle)] mb-2">후속 개념</h3>
          {linkList(d.enablesGroups, '→')}
        </section>
      )}

      <section className="card">
        <h3 className="text-xs uppercase tracking-[0.15em] text-[color:var(--color-subtle)] mb-2">상태</h3>
        <dl className="text-sm space-y-1.5">
          <div className="flex justify-between"><dt className="text-[color:var(--color-muted)]">유형</dt><dd>{d.typeLabel}</dd></div>
          <div className="flex justify-between"><dt className="text-[color:var(--color-muted)]">숙련도</dt>
            <dd><span id="masteryChip" className={`chip chip-mastery-${fm.mastery}`}>{mastery ?? d.masteryLabel}</span></dd></div>
          {d.reviewLabel && <div className="flex justify-between"><dt className="text-[color:var(--color-muted)]">복습</dt><dd><span className="chip">{d.reviewLabel}</span></dd></div>}
        </dl>
      </section>

      {d.linkedProblems.length > 0 && (
        <section className="card">
          <h3 className="text-xs uppercase tracking-[0.15em] text-[color:var(--color-subtle)] mb-2">
            {fm.concept_type === 'unit' ? `이 단원의 기출 (${d.linkedProblems.length})` : `이 개념의 기출 (${d.linkedProblems.length})`}
          </h3>
          <ul className="space-y-1 text-sm">
            {d.linkedProblems.slice(0, PREVIEW).map((p) => (
              <li key={p.slug}>
                <a className="text-[color:var(--color-accent)] hover:underline" href={`/problems/${p.slug}`}>{p.label ?? p.slug}</a>
              </li>
            ))}
          </ul>
          {d.linkedProblems.length > PREVIEW && (
            <details className="mt-2">
              <summary className="text-xs text-[color:var(--color-muted)] cursor-pointer hover:text-zinc-300">
                + {d.linkedProblems.length - PREVIEW}개 더 보기
              </summary>
              <ul className="space-y-1 text-sm mt-1">
                {d.linkedProblems.slice(PREVIEW).map((p) => (
                  <li key={p.slug}>
                    <a className="text-[color:var(--color-accent)] hover:underline" href={`/problems/${p.slug}`}>{p.label ?? p.slug}</a>
                  </li>
                ))}
              </ul>
            </details>
          )}
        </section>
      )}

      <section className="card">
        <h3 className="text-xs uppercase tracking-[0.15em] text-[color:var(--color-subtle)] mb-2">개념 지도</h3>
        <a href={`/graph?node=${encodeURIComponent(d.id)}`}
           className="block text-center px-3 py-2 rounded-md bg-indigo-500/10 hover:bg-indigo-500/20 border border-indigo-500/30 text-indigo-300 text-sm font-medium transition">
          개념 지도에서 보기 →
        </a>
      </section>

      <LearningNoteButton slug={d.id} unitTitle={fm.unit ?? d.id} collection="concepts" />

      {d.linkedSyntheses.length > 0 && (
        <section className="card">
          <h3 className="text-xs uppercase tracking-[0.15em] text-[color:var(--color-subtle)] mb-2 flex items-center gap-1.5">
            <span aria-hidden>🗒</span><span>저장된 노트</span>
            <span className="ml-auto text-[10px] font-mono text-[color:var(--color-subtle)]">{d.linkedSyntheses.length}</span>
          </h3>
          <ul className="space-y-2 text-sm">
            {d.linkedSyntheses.slice(0, 8).map((s) => (
              <li key={s.slug}>
                <a className="text-[color:var(--color-accent)] hover:underline block leading-tight"
                   href={`/syntheses/${encodeURIComponent(s.slug)}`}>{s.title}</a>
                <div className="flex items-center gap-2 mt-0.5 text-[10px] text-[color:var(--color-subtle)]">
                  {s.created && <span>{s.created}</span>}
                  {s.review_state && <span className="chip">{s.review_state}</span>}
                </div>
              </li>
            ))}
            {d.linkedSyntheses.length > 8 && (
              <li className="text-[10px] text-[color:var(--color-subtle)] pt-1 border-t border-[color:var(--color-border)]/40">
                +{d.linkedSyntheses.length - 8}개 더 — <a className="text-[color:var(--color-accent)] hover:underline" href="/syntheses">전체 보기</a>
              </li>
            )}
          </ul>
        </section>
      )}

      {fm.concept_type !== 'unit' && (
        <section className="card">
          <h3 className="text-xs uppercase tracking-[0.15em] text-[color:var(--color-subtle)] mb-2">본문 갱신</h3>
          <RegenerateBodyButton slug={d.id} noteCount={d.linkedSyntheses.length} />
        </section>
      )}
    </>
  );
}
