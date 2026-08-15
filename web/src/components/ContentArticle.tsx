// 선렌더 본문 렌더러 — 상세 페이지 4개가 공유한다.
//
// ★`dangerouslySetInnerHTML` 을 쓴다. 이 HTML 은 **우리 빌드가 만든 것**이다(사용자 입력이
//   아니다) — `docs/` 의 마크다운을 우리 remark/rehype 체인으로 구운 결과이고, 인증 뒤
//   `/api/content/...` 로만 나온다. SSR 의 `<Content />` 와 정확히 같은 바이트다.
//
// ★로딩 중에도 **높이를 잡아 둔다**. 안 그러면 본문이 늦게 들어오며 화면이 튄다(CLS).
import { useContentEntry } from '../lib/content-entry.ts';

export default function ContentArticle({ collection, id, className }: {
  collection: string; id: string; className?: string;
}) {
  const s = useContentEntry(collection, id);

  if (s.status === 'loading') {
    return <div className="min-h-[60vh] text-sm text-[color:var(--color-muted)] py-12">불러오는 중…</div>;
  }
  if (s.status === 'error') {
    return (
      <div className="card text-sm">
        <p className="font-semibold">본문을 불러오지 못했습니다.</p>
        <p className="text-xs text-[color:var(--color-muted)] mt-1 break-all">{s.message}</p>
      </div>
    );
  }
  return (
    <div className={className} dangerouslySetInnerHTML={{ __html: s.entry.html }} />
  );
}
