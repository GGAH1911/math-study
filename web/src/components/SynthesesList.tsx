// 학습 노트 목록 — Phase 3 전환 3호. 데이터는 `/api/content-index/syntheses`(방출물).
//
// ★`title`·`excerpt`·`origin_title` 은 frontmatter 가 아니라 별도 빌드 산출물에서 온다.
//   방출기가 그것을 합쳐 주므로 여기서는 그냥 읽는다(제목 정제 규칙이 그 산출물 안에 있어,
//   본문에서 다시 뽑으면 기존 화면과 미묘하게 달라진다).
import { useContentIndex, type Entry } from '../lib/content-index.ts';
import ConceptCard from './ConceptCard.tsx';

type Syn = Entry & {
  title?: string; excerpt?: string; created?: string;
  origin_concept?: string; origin_title?: string; review_state?: string;
};

const leaf = (p?: string) => (p ? (p.split('/').pop() ?? p).replace(/_/g, ' ') : '');
/** 최신순 키 — frontmatter `created` 우선, 없으면 파일명 앞 YYYY-MM-DD. SSR 과 같은 규칙이다. */
const dateOf = (s: Syn) => String(s.created ?? '').slice(0, 10) || (s.id.match(/^(\d{4}-\d{2}-\d{2})/)?.[1] ?? '');

export default function SynthesesList() {
  const s = useContentIndex<Syn>('syntheses');

  if (s.status === 'loading') {
    return <p className="text-sm text-[color:var(--color-muted)] py-12 text-center">불러오는 중…</p>;
  }
  if (s.status === 'error') {
    return (
      <div className="card text-sm">
        <p className="font-semibold">목록을 불러오지 못했습니다.</p>
        <p className="text-xs text-[color:var(--color-muted)] mt-1 break-all">{s.message}</p>
      </div>
    );
  }
  if (s.entries.length === 0) {
    return (
      <p className="text-sm text-[color:var(--color-muted)] py-12 text-center">
        아직 저장한 학습 노트가 없습니다.<br />
        컨셉 페이지에서 LLM과 대화한 뒤 "📝 학습 노트 작성 요청" → "💾 저장" 으로 만들 수 있어요.
      </p>
    );
  }

  const list = [...s.entries].sort((a, b) => dateOf(b).localeCompare(dateOf(a)));
  return (
    <ul className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {list.map((n) => {
        const originLeaf = leaf(n.origin_concept);
        const created = dateOf(n);
        return (
          <li key={n.id}>
            <ConceptCard
              href={`/syntheses/${encodeURIComponent(n.id)}`}
              title={n.title ?? n.origin_title ?? leaf(n.id)}
              subtitle={originLeaf ? `← ${originLeaf}` : undefined}
              description={n.excerpt ?? ''}
              chips={[
                ...(n.review_state ? [{ label: n.review_state }] : []),
                ...(created ? [{ label: created }] : []),
              ]}
            />
          </li>
        );
      })}
    </ul>
  );
}
