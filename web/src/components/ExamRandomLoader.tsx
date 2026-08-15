// 랜덤 모의시험 로더 — Phase 3 전환 7호. `/api/exam/random` 이 구성해 준 것을 실행한다.
//
// ★구성은 서버가 한다. 30문항 뽑으려고 코퍼스 4,210건을 받을 수 없고, 구성 규칙(난이도 가중·
//   영역 배분)이 두 곳에 있으면 앱과 웹이 다른 시험을 본다.
// ★양식·난이도 UI 는 `.astro` 에 서버 렌더로 남아 있다 — URL 파라미터만 쓰므로 코퍼스가 필요 없다.
import { useEffect, useState } from 'react';
import ExamRunner from './ExamRunner.tsx';

type Payload = { problems: React.ComponentProps<typeof ExamRunner>['problems']; durationSec: number };

export default function ExamRandomLoader({ query, title }: { query: string; title: string }) {
  const [data, setData] = useState<Payload | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    fetch(`/api/exam/random?${query}`, { headers: { accept: 'application/json' } })
      .then(async (r) => {
        if (!r.ok) {
          const b = await r.json().catch(() => ({} as { error?: string; hint?: string }));
          throw new Error(b.hint ? `${b.error} — ${b.hint}` : `HTTP ${r.status}`);
        }
        return r.json() as Promise<Payload>;
      })
      .then((d) => { if (alive) setData(d); })
      .catch((e: unknown) => { if (alive) setError(e instanceof Error ? e.message : String(e)); });
    return () => { alive = false; };
  }, [query]);

  if (error) {
    return (
      <div className="max-w-3xl mx-auto px-6 py-12 card text-sm">
        <p className="font-semibold">시험을 구성하지 못했습니다.</p>
        <p className="text-xs text-[color:var(--color-muted)] mt-1 break-all">{error}</p>
      </div>
    );
  }
  if (!data) {
    return <p className="max-w-3xl mx-auto px-6 py-16 text-center text-sm text-[color:var(--color-muted)]">시험 구성 중…</p>;
  }
  return <ExamRunner composed title={title} problems={data.problems} durationSec={data.durationSec} />;
}
