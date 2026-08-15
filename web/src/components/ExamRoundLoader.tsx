// 회차 시험 로더 — Phase 3 전환 5호. `/api/exam/round/<key>` 가 구성해 준 것을 받아 실행한다.
//
// ★정렬·응시시간 계산은 **서버가** 한다. 여기서 하면 SSR 판과 갈라지고, 앱·웹에 같은 규칙이
//   두 벌로 생긴다. 이 컴포넌트는 받아서 넘기기만 한다.
import { useEffect, useState } from 'react';
import ExamRunner from './ExamRunner.tsx';

type Payload = { title: string; problems: React.ComponentProps<typeof ExamRunner>['problems']; durationSec: number };

export default function ExamRoundLoader({ examKey }: { examKey: string }) {
  const [data, setData] = useState<Payload | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    fetch(`/api/exam/round/${examKey}`, { headers: { accept: 'application/json' } })
      .then(async (r) => {
        if (!r.ok) {
          const b = await r.json().catch(() => ({} as { error?: string; hint?: string }));
          throw new Error(b.hint ? `${b.error} — ${b.hint}` : `HTTP ${r.status}`);
        }
        return r.json() as Promise<Payload>;
      })
      .then((d) => {
        if (!alive) return;
        setData(d);
        // 껍데기는 회차명을 모른다(데이터가 있어야 안다). 받은 뒤 제목을 채운다.
        document.title = `모의시험 — ${d.title} · Math Study`;
      })
      .catch((e: unknown) => { if (alive) setError(e instanceof Error ? e.message : String(e)); });
    return () => { alive = false; };
  }, [examKey]);

  if (error) {
    return (
      <div className="max-w-3xl mx-auto px-6 py-12 card text-sm">
        <p className="font-semibold">시험을 불러오지 못했습니다.</p>
        <p className="text-xs text-[color:var(--color-muted)] mt-1 break-all">{error}</p>
        <a href="/problems" className="chip mt-4 inline-block">← 기출로</a>
      </div>
    );
  }
  if (!data) {
    return <p className="text-sm text-[color:var(--color-muted)] py-16 text-center">시험 준비 중…</p>;
  }
  return <ExamRunner title={data.title} problems={data.problems} durationSec={data.durationSec} />;
}
