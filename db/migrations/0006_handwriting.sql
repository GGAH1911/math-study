-- ── handwriting (필기 캔버스 계정화; localStorage 보완 동기화) ─────────────────
-- chat_history 패턴. 페이지별(storage_key = 'problem:<id>' | 'concept:<id>' …) user 당 1행.
-- doc = InkCanvas v2 포맷 {v,layers,strokes,activeId}. 로컬이 1차 캐시, DB 는 기기간 동기화.
CREATE TABLE IF NOT EXISTS handwriting (
  user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  storage_key TEXT NOT NULL,
  doc         JSONB NOT NULL DEFAULT '{}',
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (user_id, storage_key)
);
