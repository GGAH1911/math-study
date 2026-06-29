-- ── graph_history (그래프 패널 이력 계정화; localStorage 대체/동기화) ──────────
-- chat_history 와 동일 패턴. 단 그래프 패널은 collection/slug 없는 전역 롤링 배열이라
-- user 당 1행(entries = 최근 그래프 최대 12개 JSONB 배열). 기기 넘어 유지·캐시삭제에도 생존.
CREATE TABLE IF NOT EXISTS graph_history (
  user_id    UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  entries    JSONB NOT NULL DEFAULT '[]',
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
