// 컬렉션 목록을 클라이언트에서 가져오는 훅 — Phase 3 목록 페이지 8개가 공유한다.
//
// ★왜 훅인가(컴포넌트가 아니라): Astro 아일랜드는 **직렬화 가능한 props 만** 받는다.
//   렌더 프롭(함수)이나 JSX 를 넘기는 공통 컴포넌트는 만들 수 없다 — 넘겨도 런타임에 깨진다.
//   그래서 **가져오는 방법만** 여기 한 벌 두고, 그리는 것은 페이지별 컴포넌트가 한다.
//
// ★로딩·0건·에러를 **세 상태로** 구분한다. 이 레포에서 반복된 사고가 전부 "조용히 빈 화면"이었다.
//   로딩 중에 "없습니다"를 보여주면 사용자가 잘못 판단하고, 에러를 0건으로 보여주면 원인을 못 찾는다.
import { useEffect, useState } from 'react';

export type Entry = { id: string; [k: string]: unknown };

export type IndexState<T extends Entry> =
  | { status: 'loading' }
  | { status: 'error'; message: string }
  | { status: 'ready'; entries: T[] };

export function useContentIndex<T extends Entry>(collection: string): IndexState<T> {
  const [state, setState] = useState<IndexState<T>>({ status: 'loading' });

  useEffect(() => {
    let alive = true;
    setState({ status: 'loading' });
    // 같은 출처라 세션 쿠키가 자동으로 실린다. 앱(교차출처)은 베어러로 오고 미들웨어가 받는다 —
    // 여기서 분기할 필요가 없다.
    fetch(`/api/content-index/${collection}`, { headers: { accept: 'application/json' } })
      .then(async (r) => {
        if (!r.ok) {
          // 503 = 방출을 안 돌렸다. 서버가 실행할 명령까지 주므로 그대로 보여준다.
          const b = await r.json().catch(() => ({} as { error?: string; hint?: string }));
          throw new Error(b.hint ? `${b.error} — ${b.hint}` : `HTTP ${r.status}`);
        }
        return r.json() as Promise<{ entries?: T[] }>;
      })
      .then((d) => { if (alive) setState({ status: 'ready', entries: d.entries ?? [] }); })
      .catch((e: unknown) => {
        if (alive) setState({ status: 'error', message: e instanceof Error ? e.message : String(e) });
      });
    return () => { alive = false; };
  }, [collection]);

  return state;
}
