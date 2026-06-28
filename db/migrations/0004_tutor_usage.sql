-- ── tutor_usage (튜터 LLM 사용량·캐시 로그, 계정별) ──────────────────────
-- 튜터 1턴 호출의 토큰/캐시 메트릭을 계정별로 적재. 상용화 시 사용자별 비용·캐시 효율 추적.
-- claude --output-format stream-json 의 result 이벤트 usage 에서 추출.
-- ※ 행 데이터 — 00_ 인덱싱 대상 아님(SQL 조회). 안내는 docs/ops/status/db-metrics.md.
CREATE TABLE IF NOT EXISTS tutor_usage (
  id            BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id       UUID REFERENCES users(id) ON DELETE CASCADE,   -- NULL=미인증(드물게)
  collection    TEXT,                                          -- 'concepts' | 'problems' | 'dashboard'
  slug          TEXT,
  model         TEXT,                                          -- 'haiku' | 'sonnet' | byok 모델
  byok          BOOLEAN NOT NULL DEFAULT FALSE,
  input_tokens         INT NOT NULL DEFAULT 0,
  output_tokens        INT NOT NULL DEFAULT 0,
  cache_read_tokens    INT NOT NULL DEFAULT 0,                 -- ★프롬프트 캐시 히트(높을수록 절약)
  cache_creation_tokens INT NOT NULL DEFAULT 0,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 계정별 최근 조회·집계용.
CREATE INDEX IF NOT EXISTS idx_tutor_usage_user_time ON tutor_usage (user_id, created_at DESC);
