// 기출 상세 좌측 컬럼 — Phase 3 전환 11호(A그룹 3/4). 데이터는 `/api/problems/<slug>`.
//
// ★기존 아일랜드(InkCanvas·ProblemAttemptPanel·SolutionPanel·Geometry)를 **이 안의 평범한
//   자식 컴포넌트**로 넣는다. 섬 안에서는 `client:` 지시자가 필요 없고, 직렬화 제약도 사라진다 —
//   쪼개서 각자 fetch 하게 만드는 것보다 단순하고 요청도 한 번이다.
//
// ★재구성 토글은 원래 인라인 스크립트였다. React 상태로 옮겨 DOM 을 직접 만지지 않는다.
//   (서버 렌더 시절 `hidden` 속성을 토글하던 코드는 클라이언트 렌더에서 타이밍 함정이 된다.)
import { useEffect, useState } from 'react';
import RoundNav, { type NavItem } from './RoundNav.tsx';
import InkCanvas from './InkCanvas.tsx';
import ProblemAttemptPanel from './ProblemAttemptPanel.tsx';
import SolutionPanel from './SolutionPanel.tsx';
import Geometry from './Geometry.tsx';
import { yearLabel, FORMAT_LABEL, TIER_BADGE } from '../lib/problem-meta';
import { STATUS_LABEL_KO } from '../lib/srs.ts';

type Detail = {
  id: string;
  data: Record<string, any>;
  html: string;
  unitTitle: string; subjLabel: string; has3D: boolean; isAdmin: boolean;
  wholeStem: string | null;
  recon: { html: string; gStmtHtml: string; gChoiceHtml: string; hasGeo: boolean; geo: unknown; full: string };
  roundNav: { prev: NavItem | null; nexts: NavItem[]; curSubject: string; currentLabel: string };
  concepts: Array<{ ref: string; label: string; resolved: string | null }>;
};

const day = (d?: string) => (d ? String(d).slice(0, 10) : null);

export default function ProblemDetail({ slug }: { slug: string }) {
  const [d, setD] = useState<Detail | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [view, setView] = useState<'raw' | 'recon'>('raw');

  useEffect(() => {
    let alive = true;
    const path = slug.split('/').map(encodeURIComponent).join('/');
    fetch(`/api/problems/${path}`, { headers: { accept: 'application/json' } })
      .then(async (r) => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json() as Promise<Detail>; })
      .then((v) => { if (alive) { setD(v); document.title = `${v.unitTitle} · Math Study`; } })
      .catch((e: unknown) => { if (alive) setError(e instanceof Error ? e.message : String(e)); });
    return () => { alive = false; };
  }, [slug]);

  if (error) {
    return (
      <div className="card text-sm">
        <p className="font-semibold">문제를 불러오지 못했습니다.</p>
        <p className="text-xs text-[color:var(--color-muted)] mt-1 break-all">{error}</p>
        <a href="/problems" className="chip mt-4 inline-block">← 기출로</a>
      </div>
    );
  }
  if (!d) return <div className="min-h-[60vh] text-sm text-[color:var(--color-muted)] py-12">불러오는 중…</div>;

  const fm = d.data;
  const src = fm.source;
  const hasRecon = !!d.recon.html;

  return (
    <>
      <RoundNav {...d.roundNav} />

      <article className="max-w-none mt-4">
        {d.has3D && (
          <button type="button" id="ask-3d"
            className="inline-flex items-center gap-1.5 mb-4 mr-3 px-3 py-1.5 rounded-lg border border-[color:var(--color-border)] text-sm font-medium hover:bg-[color:var(--color-surface-2)]"
            title="튜터가 이 문제의 입체 도형을 바로 그려 줍니다">
            <span aria-hidden="true">🧊</span> 입체로 보기
          </button>
        )}

        {hasRecon && (
          <div className="prob-toggle inline-flex rounded-lg border border-[color:var(--color-border)] overflow-hidden mb-4 text-sm" role="tablist" aria-label="문제 보기 방식">
            <button type="button" className={`px-3.5 py-1.5 font-medium${view === 'raw' ? ' bg-[color:var(--color-surface-2)]' : ''}`}
                    onClick={() => setView('raw')}>🖼 원본 이미지</button>
            <button type="button" className={`px-3.5 py-1.5 font-medium border-l border-[color:var(--color-border)]${view === 'recon' ? ' bg-[color:var(--color-surface-2)]' : ''}`}
                    onClick={() => setView('recon')}>✦ 재구성</button>
          </div>
        )}

        {view === 'raw' && (
          // 우리 빌드가 구운 HTML(사용자 입력 아님) — SSR 의 `<Content />` 와 같은 바이트다.
          <div className="prose prose-invert max-w-none" dangerouslySetInnerHTML={{ __html: d.html }} />
        )}

        {hasRecon && view === 'recon' && (
          <div className="recon-view">
            <div className="recon-head">
              <span className="recon-num">{src?.number ?? ''}.</span>
              {src?.score && <span className="recon-score">[{src.score}점]</span>}
            </div>
            {d.recon.hasGeo ? (
              <>
                <div dangerouslySetInnerHTML={{ __html: d.recon.gStmtHtml }} />
                {d.recon.geo ? (
                  <div className="recon-fig-wrap">
                    <Geometry spec={d.recon.geo as never} width={520} height={420} hideCaption noBroadcast />
                  </div>
                ) : null}
                {fm.choice_figures?.length ? (
                  <div className="recon-choices recon-choices-img">
                    {fm.choice_figures.map((c: { label: string; image: string }) => (
                      <div className="recon-choice-fig" key={c.label}>
                        <span className="recon-choice-label">{c.label}</span>
                        <img src={c.image} alt={`보기 ${c.label}`} loading="lazy" />
                      </div>
                    ))}
                  </div>
                ) : (d.recon.gChoiceHtml && <div dangerouslySetInnerHTML={{ __html: d.recon.gChoiceHtml }} />)}
              </>
            ) : (
              <div dangerouslySetInnerHTML={{ __html: d.recon.full }} />
            )}
          </div>
        )}

        {/* 손풀이 — 좌하단 floating FAB(InkCanvas 내부 렌더). 래퍼는 마운트 지점일 뿐이다. */}
        <div className="not-prose">
          <InkCanvas storageKey={`problem:${d.id}`}
                     bgImage={d.wholeStem ? `/problem-images/${d.wholeStem}` : undefined}
                     launchLabel="손으로 풀이" />
        </div>
        <div className="my-6"><ProblemAttemptPanel slug={d.id} /></div>
        <SolutionPanel solution={fm.solution} />
      </article>

      {/* 메타데이터 — 우측 rail 은 채팅이 쓰므로 문제 아래 가로 카드로. */}
      <div className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        <section className="card">
          <h3 className="text-xs uppercase tracking-[0.15em] text-[color:var(--color-subtle)] mb-2">상태</h3>
          <dl className="text-sm space-y-1.5">
            <div className="flex justify-between"><dt className="text-[color:var(--color-muted)]">상태</dt>
              <dd><span className={`chip chip-status-${fm.status}`}>{STATUS_LABEL_KO[fm.status] ?? fm.status}</span></dd></div>
            {fm.format && <div className="flex justify-between"><dt className="text-[color:var(--color-muted)]">유형</dt><dd>{FORMAT_LABEL[fm.format] ?? fm.format}</dd></div>}
            {fm.killer_tier && <div className="flex justify-between"><dt className="text-[color:var(--color-muted)]">난이도</dt>
              <dd><span className={`chip ${TIER_BADGE[fm.killer_tier]?.cls ?? ''}`}>{TIER_BADGE[fm.killer_tier]?.text ?? fm.killer_tier}</span></dd></div>}
            {fm.cognitive_type && <div className="flex justify-between"><dt className="text-[color:var(--color-muted)]">인지 유형</dt><dd>{fm.cognitive_type}</dd></div>}
            {fm.answer && (
              <div className="flex justify-between items-center"><dt className="text-[color:var(--color-muted)]">정답</dt>
                <dd>
                  <button type="button"
                    className="answer-blur font-mono text-sm px-2 py-0.5 rounded border border-[color:var(--color-border)] bg-[color:var(--color-surface-2)] hover:border-[color:var(--color-accent)] transition cursor-pointer"
                    data-answer={fm.answer} aria-label="정답 보기"
                    onClick={(e) => e.currentTarget.classList.toggle('revealed')}>{fm.answer}</button>
                </dd>
              </div>
            )}
            {fm.official_pass_rate && <div className="flex justify-between"><dt className="text-[color:var(--color-muted)]">정답률</dt><dd>{fm.official_pass_rate}%</dd></div>}
            {fm.difficulty && <div className="flex justify-between"><dt className="text-[color:var(--color-muted)]">난이도</dt><dd>{fm.difficulty}</dd></div>}
            {day(fm.next_review) && <div className="flex justify-between"><dt className="text-[color:var(--color-muted)]">다음 복습</dt><dd>{day(fm.next_review)}</dd></div>}
          </dl>
          {fm.exam_intent && (
            <p className="mt-3 pt-3 border-t border-[color:var(--color-border)] text-xs text-[color:var(--color-muted)] leading-relaxed">🎯 {fm.exam_intent}</p>
          )}
        </section>

        {src && (
          <section className="card">
            <h3 className="text-xs uppercase tracking-[0.15em] text-[color:var(--color-subtle)] mb-2">출처</h3>
            <dl className="text-sm space-y-1">
              <div className="flex justify-between"><dt className="text-[color:var(--color-muted)]">시행</dt><dd>{src.agency} · {src.exam_type}</dd></div>
              <div className="flex justify-between"><dt className="text-[color:var(--color-muted)]">회차</dt>
                <dd>{yearLabel(src.year, src.exam_type)}{src.session ? ` · ${src.session}` : ''}</dd></div>
              <div className="flex justify-between"><dt className="text-[color:var(--color-muted)]">과목</dt><dd>{src.subject}</dd></div>
              <div className="flex justify-between"><dt className="text-[color:var(--color-muted)]">번호</dt><dd>{src.number}번 · {src.score ?? '?'}점</dd></div>
            </dl>
          </section>
        )}

        {d.concepts.length > 0 && (
          <section className="card">
            <h3 className="text-xs uppercase tracking-[0.15em] text-[color:var(--color-subtle)] mb-2">매핑된 개념</h3>
            <ul className="space-y-1.5 text-sm">
              {d.concepts.map((c) => (
                <li key={c.ref}>
                  {c.resolved
                    ? <a className="text-[color:var(--color-accent)] hover:underline" href={`/concepts/${c.resolved}`}>{c.label}</a>
                    : <span className="text-[color:var(--color-subtle)]" title="아직 개념 노드가 없는 태그">{c.label}</span>}
                </li>
              ))}
            </ul>
          </section>
        )}
      </div>
    </>
  );
}
