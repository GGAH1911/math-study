// 학습 경로 — Phase 3 C그룹. 계산은 `/api/learning-path` 가 한다(그래프 알고리즘).
//
// ★목표를 바꾸면 URL 이 바뀌고 그에 맞춰 다시 부른다. 서버 왕복 없이 경로만 갈아끼운다 —
//   원래는 `?goal=` 마다 페이지가 통째로 다시 렌더됐다.
import { useEffect, useState } from 'react';
import PathPicker from './PathPicker.tsx';
import MetroMap, { type PathNodeVM, type PathEdgeVM } from './MetroMap.tsx';

type Path = {
  goal: { id: string; label: string } | null; missingGoal?: boolean;
  totalPrereqs: number; donePrereqs: number;
  nodes: PathNodeVM[]; edges: PathEdgeVM[];
};
type Data = { concepts: unknown[]; quickGoals: Array<{ id: string; label: string }>; path: Path | null };

export default function LearningPath({ goal }: { goal: string }) {
  const [d, setD] = useState<Data | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    const q = goal ? `?goal=${encodeURIComponent(goal)}` : '';
    fetch(`/api/learning-path${q}`, { headers: { accept: 'application/json' } })
      .then(async (r) => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json() as Promise<Data>; })
      .then((v) => { if (alive) setD(v); })
      .catch((e: unknown) => { if (alive) setError(e instanceof Error ? e.message : String(e)); });
    return () => { alive = false; };
  }, [goal]);

  if (error) {
    return (
      <div className="card text-sm">
        <p className="font-semibold">학습 경로를 불러오지 못했습니다.</p>
        <p className="text-xs text-[color:var(--color-muted)] mt-1 break-all">{error}</p>
      </div>
    );
  }
  if (!d) return <p className="text-sm text-[color:var(--color-muted)] py-12 text-center">불러오는 중…</p>;

  const p = d.path;
  const todoCount = p ? p.nodes.filter((n) => !n.isGoal).length : 0;

  return (
    <>
      <section className="card space-y-3">
        <PathPicker concepts={d.concepts as never} />
        {d.quickGoals.length > 0 && (
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs text-[color:var(--color-subtle)]">예시 목표:</span>
            {d.quickGoals.map((g) => (
              <a key={g.id} href={`/paths?goal=${encodeURIComponent(g.id)}`} className="chip hover:border-[color:var(--color-accent)]">{g.label}</a>
            ))}
          </div>
        )}
      </section>

      {p?.missingGoal && (
        <p className="card text-sm text-[color:var(--color-muted)]">해당 개념을 찾지 못했습니다. 위 검색에서 다시 골라주세요.</p>
      )}

      {p?.goal && (
        <section className="space-y-4">
          <div className="flex items-baseline justify-between gap-3 flex-wrap">
            <h2 className="text-lg font-semibold">
              목표: <a href={`/concepts/${p.goal.id}`} className="text-[color:var(--color-accent)] hover:underline">{p.goal.label}</a>
            </h2>
            <p className="text-xs text-[color:var(--color-muted)]">
              선행 {p.totalPrereqs}개 중 {p.donePrereqs}개 이수 · <strong>{todoCount}개 학습 필요</strong>
            </p>
          </div>
          {todoCount === 0 ? (
            <p className="card text-sm">
              선행 개념을 모두 익혔습니다 🎉 바로
              <a href={`/concepts/${p.goal.id}`} className="text-[color:var(--color-accent)] hover:underline"> 목표 개념</a>을 학습하세요.
            </p>
          ) : (
            <MetroMap nodes={p.nodes} edges={p.edges} totalPrereqs={p.totalPrereqs} donePrereqs={p.donePrereqs} todoCount={todoCount} />
          )}
        </section>
      )}

      {!p && (
        <p className="text-sm text-[color:var(--color-subtle)]">
          위에서 목표를 고르면 경로가 생성됩니다. 예: 「도함수의 활용」을 목표로 하면 함수·극한·미분 선행 개념이 순서대로 나열됩니다.
        </p>
      )}
    </>
  );
}
