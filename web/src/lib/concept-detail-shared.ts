// 개념 상세 — 공유 타입과 데이터 훅. 본문 섬과 서랍 섬이 **같은 요청**을 쓴다.
import { useJsonOnce, type JsonState } from './content-entry.ts';

type Item = { slug: string; label: string };
export type Group = { label: string; items: Item[] };
type ProblemBrief = { slug: string; label?: string; tier?: string; [k: string]: unknown };
type Syn = { slug: string; title: string; created?: string; review_state?: string };
export type Detail = {
  id: string; data: Record<string, any>; html: string; title: string;
  typeLabel: string; masteryLabel: string; reviewLabel: string | null;
  prereqGroups: Group[]; enablesGroups: Group[];
  conceptFigure: unknown; conceptFigure3d: unknown; conceptWidgetSpec: unknown;
  linkedProblems: ProblemBrief[]; linkedSyntheses: Syn[];
  hasWidgetOf: Record<string, boolean>;
};


export const PREVIEW = 8;

/** 두 섬이 같은 URL 을 부르면 요청은 한 번이다(loadJsonOnce 캐시). */
export function useConceptDetail(slug: string): JsonState<Detail> {
  const path = slug.split('/').map(encodeURIComponent).join('/');
  return useJsonOnce<Detail>(`/api/concepts/${path}`);
}

/** "## 본문" 헤딩(없으면 첫 blockquote 끝) 앞에서 자른다. 못 찾으면 통째로 앞부분.
 *  ★원래는 인라인 스크립트가 `#conceptBody` 를 찾아 DOM 을 **옮겼다.** 클라이언트 렌더에선
 *    그 시점에 본문이 없어 안 먹는다 — 잘라 끼우는 쪽이 타이밍에 기대지 않아 안전하다. */
export function splitAtBody(html: string): [string, string] {
  const h2 = html.search(/<h2[^>]*>\s*본문/);
  if (h2 >= 0) return [html.slice(0, h2), html.slice(h2)];
  const bq = html.indexOf('</blockquote>');
  if (bq >= 0) return [html.slice(0, bq + 13), html.slice(bq + 13)];
  return [html, ''];
}
