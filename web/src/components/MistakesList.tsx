// 오답노트 목록 — Phase 3 전환 2호. 데이터는 `/api/content-index/mistakes`(방출물).
import { useContentIndex, type Entry } from '../lib/content-index.ts';
import ConceptCard from './ConceptCard.tsx';

type Mistake = Entry & { error_type?: string; lesson?: string; problem?: string; revisit_date?: string };

const leaf = (p?: string) => (p ? (p.split('/').pop() ?? p).replace(/\.md$/, '') : '—');
// 방출물의 날짜는 JSON 이라 **문자열**이다(SSR 은 Date 객체였다). ISO 앞 10자만 쓴다.
const day = (d?: string) => (d ? String(d).slice(0, 10) : '—');

export default function MistakesList() {
  const s = useContentIndex<Mistake>('mistakes');

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
    return <p className="text-sm text-[color:var(--color-muted)] py-12 text-center">아직 오답 노트가 없습니다.</p>;
  }

  const list = [...s.entries].sort((a, b) => a.id.localeCompare(b.id, 'ko-KR'));
  return (
    <ul className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {list.map((m) => (
        <li key={m.id}>
          <ConceptCard
            href={`/mistakes/${encodeURIComponent(m.id)}`}
            title={m.id}
            chips={m.error_type ? [{ label: m.error_type, class: `chip-error-${m.error_type}` }] : []}
            description={m.lesson ?? ''}
            meta={[
              { key: '문제', value: leaf(m.problem) },
              { key: '복습', value: day(m.revisit_date) },
            ]}
          />
        </li>
      ))}
    </ul>
  );
}
