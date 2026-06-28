// 튜터 대화 이력 영속 — localStorage(빠른 캐시) + DB(계정별·기기간). ChatPanel 에서 분리.
import type { ChatMessage } from './types';

export const STORAGE_PREFIX = 'math-study:chat:';
export const MAX_HISTORY_TURNS = 12; // include up to last N messages in API request

// sub-dir 진입 후 호환: 'algebra/근의_공식' 같은 새 slug 로 로딩 시,
// 기존 flat slug 'math-study:chat:근의_공식' 도 fallback 으로 확인하고 lazy 이전.
export function loadHistory(slug: string): ChatMessage[] {
  if (typeof window === 'undefined') return [];
  try {
    const newKey = STORAGE_PREFIX + slug;
    const raw = window.localStorage.getItem(newKey);
    if (raw) return JSON.parse(raw) as ChatMessage[];
    if (slug.includes('/')) {
      const leaf = slug.split('/').pop() ?? slug;
      const legacyKey = STORAGE_PREFIX + leaf;
      const legacy = window.localStorage.getItem(legacyKey);
      if (legacy) {
        window.localStorage.setItem(newKey, legacy);
        window.localStorage.removeItem(legacyKey);
        return JSON.parse(legacy) as ChatMessage[];
      }
    }
    return [];
  } catch {
    return [];
  }
}

export function saveHistory(slug: string, msgs: ChatMessage[]): void {
  try {
    // 이미지 dataURL 은 용량이 커 localStorage quota 를 빠르게 소진 → 저장 시 제외.
    const slim = msgs.map((m) => (m.images?.length ? { ...m, images: undefined } : m));
    window.localStorage.setItem(STORAGE_PREFIX + slug, JSON.stringify(slim));
  } catch {
    /* quota or disabled — ignore */
  }
}

// 대화 이력 DB 동기화(계정별 · 기기 넘어 유지). localStorage 는 빠른 캐시로 병행.
export async function loadDbHistory(collection: string, slug: string): Promise<ChatMessage[] | null> {
  try {
    const r = await fetch(`/api/chat-history?collection=${encodeURIComponent(collection)}&slug=${encodeURIComponent(slug)}`);
    if (!r.ok) return null;
    const d = await r.json();
    return Array.isArray(d.messages) ? (d.messages as ChatMessage[]) : null;
  } catch { return null; }
}

export function saveDbHistory(collection: string, slug: string, msgs: ChatMessage[]): void {
  try {
    const slim = msgs.map((m) => (m.images?.length ? { ...m, images: undefined } : m));
    fetch('/api/chat-history', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ collection, slug, messages: slim }),
    }).catch(() => { /* offline/실패 무시 — localStorage 에 캐시됨 */ });
  } catch { /* ignore */ }
}
