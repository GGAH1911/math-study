// 선렌더 콘텐츠 1건을 가져오는 훅 — 상세 페이지 4개(A그룹)가 공유한다.
//
// ★한 페이지에서 **섬이 둘 이상** 같은 문서를 쓴다(본문 + 우측 서랍의 메타). 각자 fetch 하면
//   같은 요청이 두 번 나간다 — 브라우저 캐시는 **동시** 요청을 합쳐 주지 않는다.
//   그래서 모듈 수준에서 **약속(Promise)을 공유**한다. 두 번째 호출자는 같은 약속을 받는다.
//
// ★`ContextDrawer` 의 껍데기와 개폐 스크립트는 `.astro` 에 서버 렌더로 남긴다. 그쪽을 섬으로
//   옮기면 스크립트가 빈 DOM 을 훑는 타이밍 함정(ProblemFilters 와 동일)을 또 만든다.
import { useEffect, useState } from 'react';

export type ContentEntry<D = Record<string, unknown>> = {
  id: string;
  collection: string;
  data: D;
  html: string;
};

const cache = new Map<string, Promise<ContentEntry>>();

/** 같은 (컬렉션, id) 는 요청 한 번. 페이지가 살아 있는 동안 유효하다. */
export function loadContentEntry(collection: string, id: string): Promise<ContentEntry> {
  const key = `${collection}/${id}`;
  const hit = cache.get(key);
  if (hit) return hit;
  // ★id 는 세그먼트별로 인코딩한다. 통째로 하면 `/` 가 %2F 가 돼 경로가 무너진다.
  const path = id.split('/').map(encodeURIComponent).join('/');
  const p = fetch(`/api/content/${collection}/${path}`, { headers: { accept: 'application/json' } })
    .then(async (r) => {
      if (!r.ok) {
        const b = await r.json().catch(() => ({} as { error?: string; hint?: string }));
        throw new Error(b.hint ? `${b.error} — ${b.hint}` : `HTTP ${r.status}`);
      }
      return r.json() as Promise<ContentEntry>;
    });
  // 실패한 약속을 캐시에 남기면 재시도가 영원히 막힌다.
  p.catch(() => cache.delete(key));
  cache.set(key, p);
  return p;
}

export type EntryState<D> =
  | { status: 'loading' }
  | { status: 'error'; message: string }
  | { status: 'ready'; entry: ContentEntry<D> };

export function useContentEntry<D = Record<string, unknown>>(collection: string, id: string): EntryState<D> {
  const [s, setS] = useState<EntryState<D>>({ status: 'loading' });
  useEffect(() => {
    let alive = true;
    setS({ status: 'loading' });
    loadContentEntry(collection, id)
      .then((e) => { if (alive) setS({ status: 'ready', entry: e as ContentEntry<D> }); })
      .catch((e: unknown) => { if (alive) setS({ status: 'error', message: e instanceof Error ? e.message : String(e) }); });
    return () => { alive = false; };
  }, [collection, id]);
  return s;
}

// ── 임의 JSON 엔드포인트용 공유 캐시 ────────────────────────────────────────
// ★상세 페이지는 한 화면에서 섬이 둘(본문 + 서랍)이고 **같은 엔드포인트**를 쓴다.
//   각자 fetch 하면 요청이 두 번 나간다 — 브라우저 캐시는 동시 요청을 합쳐 주지 않는다.
const jsonCache = new Map<string, Promise<unknown>>();

export function loadJsonOnce<T>(url: string): Promise<T> {
  const hit = jsonCache.get(url);
  if (hit) return hit as Promise<T>;
  const p = fetch(url, { headers: { accept: 'application/json' } }).then(async (r) => {
    const body = await r.json().catch(() => ({}));
    if (!r.ok) throw Object.assign(new Error(String((body as { error?: string }).error ?? `HTTP ${r.status}`)), { status: r.status, body });
    return body as T;
  });
  p.catch(() => jsonCache.delete(url));   // 실패를 캐시에 남기면 재시도가 영원히 막힌다
  jsonCache.set(url, p);
  return p;
}

export type JsonState<T> =
  | { status: 'loading' }
  | { status: 'error'; message: string; body?: unknown }
  | { status: 'ready'; data: T };

export function useJsonOnce<T>(url: string): JsonState<T> {
  const [s, setS] = useState<JsonState<T>>({ status: 'loading' });
  useEffect(() => {
    let alive = true;
    setS({ status: 'loading' });
    loadJsonOnce<T>(url)
      .then((data) => { if (alive) setS({ status: 'ready', data }); })
      .catch((e: unknown) => {
        if (!alive) return;
        const err = e as Error & { body?: unknown };
        setS({ status: 'error', message: err.message, body: err.body });
      });
    return () => { alive = false; };
  }, [url]);
  return s;
}
