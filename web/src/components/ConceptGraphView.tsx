// 개념 지도 — Phase 3 C그룹. 데이터는 `/api/concept-graph`(그래프 + 사용자 mastery + 노트수).
import { useEffect, useState } from 'react';
import ConceptDAG from './ConceptDAG.tsx';

type Graph = { stats?: { nodes?: number }; nodes?: unknown[]; edges?: unknown[] };

export default function ConceptGraphView({ highlight }: { highlight?: string }) {
  const [g, setG] = useState<Graph | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    fetch('/api/concept-graph', { headers: { accept: 'application/json' } })
      .then(async (r) => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json() as Promise<Graph>; })
      .then((v) => { if (alive) setG(v); })
      .catch((e: unknown) => { if (alive) setError(e instanceof Error ? e.message : String(e)); });
    return () => { alive = false; };
  }, []);

  if (error) {
    return (
      <div className="flex items-center justify-center h-full text-[color:var(--color-muted)]">
        <div className="text-center">
          <p className="text-lg">개념 지도를 불러오지 못했습니다.</p>
          <p className="text-xs mt-1 break-all">{error}</p>
        </div>
      </div>
    );
  }
  if (!g) {
    return <div className="flex items-center justify-center h-full text-sm text-[color:var(--color-muted)]">불러오는 중…</div>;
  }
  if (!g.stats?.nodes) {
    return (
      <div className="flex items-center justify-center h-full text-[color:var(--color-muted)]">
        <div className="text-center">
          <div className="text-5xl mb-3">◈</div>
          <p className="text-lg">아직 개념 지도가 비어 있습니다.</p>
          <p className="text-sm mt-1">docs/concepts/ 에 첫 개념을 시드해주세요.</p>
        </div>
      </div>
    );
  }
  return <ConceptDAG data={g as never} variant="full" highlight={highlight} />;
}
