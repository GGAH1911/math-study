// 학습 자료 목록 — Phase 3 전환 1호. 데이터는 `/api/content-index/tools`(방출물)에서 온다.
//
// ★페이지(`tools.astro`)에는 제목·h1 만 남긴다. 목록만 여기로 온 이유는 두 가지다:
//   ① 사용자가 JS 로딩 전에도 어느 화면인지 본다
//   ② 라우트 스냅샷이 title·h1 로 계속 회귀를 잰다 — 전부 옮기면 원본 HTML 이 비어 못 잰다.
import { useContentIndex, type Entry } from '../lib/content-index.ts';

type Tool = Entry & { title?: string; kind?: string; url?: string };

export default function ToolsList() {
  const s = useContentIndex<Tool>('tools');

  if (s.status === 'loading') {
    return <div className="card text-sm text-[color:var(--color-muted)] py-8 text-center">불러오는 중…</div>;
  }
  if (s.status === 'error') {
    // 에러를 0건으로 뭉개지 않는다 — 그러면 "자료가 없다"로 잘못 읽힌다.
    return (
      <div className="card text-sm">
        <p className="font-semibold">목록을 불러오지 못했습니다.</p>
        <p className="text-xs text-[color:var(--color-muted)] mt-1 break-all">{s.message}</p>
      </div>
    );
  }
  if (s.entries.length === 0) {
    return (
      <div className="card text-center py-12">
        <p className="text-base">아직 등록된 학습 자료가 없습니다.</p>
        <p className="text-sm text-[color:var(--color-muted)] mt-2">
          외부 자료를 추가하려면 <code className="text-[color:var(--color-accent)]">docs/tools/</code>에 markdown 페이지를 만들고
          frontmatter에 <code className="text-[color:var(--color-accent)]">kind</code>·
          <code className="text-[color:var(--color-accent)]">title</code>·
          <code className="text-[color:var(--color-accent)]">url</code> 등을 적어주세요.
        </p>
      </div>
    );
  }

  return (
    <ul className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {s.entries.map((t) => (
        <li key={t.id} className="card">
          <h3 className="font-semibold">{t.title ?? t.id}</h3>
          {t.kind && <span className="chip mt-2">{t.kind}</span>}
          {t.url && (
            <a href={t.url} className="text-xs text-[color:var(--color-accent)] hover:underline mt-2 block truncate"
               target="_blank" rel="noopener noreferrer">{t.url}</a>
          )}
        </li>
      ))}
    </ul>
  );
}
