// 개념 상세 — 본문 섬. 도식·위젯을 본문 **사이에 끼워** 렌더한다(DOM 이동 아님).
import { useEffect, useMemo } from 'react';
import { useConceptDetail, splitAtBody } from '../lib/concept-detail-shared.ts';
import Geometry from './Geometry.tsx';
import Geometry3D from './Geometry3D.tsx';
import ConceptWidget from './ConceptWidget.tsx';
import InkCanvas from './InkCanvas.tsx';

export default function ConceptArticle({ slug }: { slug: string }) {
  const s = useConceptDetail(slug);
  const d = s.status === 'ready' ? s.data : null;
  const [head, tail] = useMemo(() => (d ? splitAtBody(d.html) : ['', '']), [d]);

  useEffect(() => {
    if (d) document.title = `${d.title} · Math Study`;
  }, [d]);

  // flat-leaf 로 들어왔으면 정식 경로로 이동한다(SSR 이 302 로 하던 것).
  useEffect(() => {
    if (s.status !== 'error') return;
    const canonical = (s.body as { canonical?: string } | undefined)?.canonical;
    if (canonical) location.replace(encodeURI(`/concepts/${canonical}`));
  }, [s]);

  if (s.status === 'error') {
    if ((s.body as { canonical?: string } | undefined)?.canonical) {
      return <div className="min-h-[40vh] text-sm text-[color:var(--color-muted)] py-12">이동 중…</div>;
    }
    return (
      <div className="card text-sm">
        <p className="font-semibold">개념을 불러오지 못했습니다.</p>
        <p className="text-xs text-[color:var(--color-muted)] mt-1 break-all">{s.message}</p>
        <a href="/concepts" className="chip mt-4 inline-block">← 개념으로</a>
      </div>
    );
  }
  if (!d) return <div className="min-h-[60vh] text-sm text-[color:var(--color-muted)] py-12">불러오는 중…</div>;

  return (
    <>
      <div className="prose prose-invert max-w-none" dangerouslySetInnerHTML={{ __html: head }} />

      {(d.conceptFigure || d.conceptFigure3d) && (
        // 3D 와 2D 가 둘 다 있으면 둘 다 — 3D 먼저(입체가 개념의 핵심).
        <figure className="not-prose my-6 flex flex-col items-center gap-3">
          {d.conceptFigure3d ? (
            <div className="w-full flex justify-center rounded-lg border border-zinc-700/60 bg-zinc-950/40 p-3">
              <Geometry3D spec={d.conceptFigure3d as never} width={720} height={480} hideCaption />
            </div>
          ) : null}
          {d.conceptFigure ? (
            <div className="w-full flex justify-center rounded-lg border border-zinc-700/60 bg-zinc-950/40 p-3">
              <Geometry spec={d.conceptFigure as never} width={1400} height={760} hideCaption />
            </div>
          ) : null}
        </figure>
      )}

      <div className="not-prose">
        <ConceptWidget conceptId={d.id} spec={d.conceptWidgetSpec as never} />
      </div>

      {tail && <div className="prose prose-invert max-w-none" dangerouslySetInnerHTML={{ __html: tail }} />}

      <div className="not-prose">
        <InkCanvas storageKey={`concept:${d.id}`} launchLabel="필기" />
      </div>
    </>
  );
}
