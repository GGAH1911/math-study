-- 0003: 멤버십 / 멀티유저 — auth + 사용자별 학습자 모델 + 대화이력
--
-- 추가형(additive). 기존 problem_state/problem_attempts 데이터 보존:
-- 그 행들의 user_id(SINGLE_USER_ID)를 'legacy' 플레이스홀더 유저로 흡수해 FK 유효성을
-- 확보하고, 첫 실(實)가입 계정이 인수(claim)한다(앱 로직). 비번 해싱은 앱(crypto.scrypt).
-- 이메일은 citext 대신 lower(email) 유니크 인덱스로 대소문자 무시(extension 의존성 회피).

BEGIN;

-- ── users ──────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
  id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email          TEXT NOT NULL,
  password_hash  TEXT,                          -- scrypt$N$r$p$salt$hash; NULL=OAuth전용/legacy
  oauth_provider TEXT,                          -- 'google' 등
  oauth_subject  TEXT,                          -- provider 의 안정적 user id (sub)
  display_name   TEXT,
  is_active      BOOLEAN NOT NULL DEFAULT TRUE,
  is_legacy      BOOLEAN NOT NULL DEFAULT FALSE,-- 기존 single-user 데이터 보유 플레이스홀더
  created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  last_login_at  TIMESTAMPTZ
);
COMMENT ON TABLE users IS '회원 계정. password_hash=scrypt(NULL이면 OAuth/legacy). is_legacy=기존 single-user 데이터 보유 플레이스홀더(로그인 불가).';

-- 대소문자 무시 이메일 유니크 (앱에서도 lower 후 비교)
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email_lower ON users (lower(email));
-- OAuth 식별자 유니크 (provider+sub). 둘 다 NULL(비번유저)이면 유니크에서 제외.
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_oauth ON users (oauth_provider, oauth_subject)
  WHERE oauth_provider IS NOT NULL AND oauth_subject IS NOT NULL;

-- legacy 플레이스홀더: 기존 problem_state/attempts 의 SINGLE_USER_ID 흡수.
-- password_hash NULL → 로그인 불가. 첫 실가입 시 데이터 인수 후 정리.
INSERT INTO users (id, email, display_name, is_legacy, is_active, password_hash)
VALUES ('00000000-0000-0000-0000-000000000001', 'legacy@math-study.local',
        '기존 데이터(이관 대기)', TRUE, FALSE, NULL)
ON CONFLICT (id) DO NOTHING;

-- ── sessions (DB 백업 세션) ─────────────────────────────────────────
-- 쿠키엔 랜덤 토큰 원본, DB엔 sha256(token)만 저장 → DB 유출돼도 세션 위조 불가.
CREATE TABLE IF NOT EXISTS sessions (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token_hash  TEXT NOT NULL UNIQUE,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  expires_at  TIMESTAMPTZ NOT NULL,
  user_agent  TEXT,
  ip          TEXT
);
CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_exp  ON sessions(expires_at);

-- ── concept_mastery (사용자별 개념 숙달; frontmatter 전역값 대체) ────
CREATE TABLE IF NOT EXISTS concept_mastery (
  user_id          UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  concept_id       TEXT NOT NULL,               -- concept slug = content c.id (중첩경로)
  mastery          TEXT NOT NULL DEFAULT 'unknown',
  mastery_evidence JSONB NOT NULL DEFAULT '[]',
  mastery_updated  TIMESTAMPTZ,
  review_state     TEXT,
  next_review      DATE,
  PRIMARY KEY (user_id, concept_id),
  CHECK (mastery IN ('unknown','learning','proficient','mastered'))
);
CREATE INDEX IF NOT EXISTS idx_cm_user ON concept_mastery(user_id);

-- ── user_profile (정성 학습자 프로필; 튜터가 갱신) ──────────────────
CREATE TABLE IF NOT EXISTS user_profile (
  user_id             UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  self_reported_level TEXT,                     -- 학생 자기보고 수준(있으면)
  goals               TEXT,                     -- 학습 목표
  weakness_patterns   JSONB NOT NULL DEFAULT '[]', -- 약점 패턴 누적(튜터 갱신)
  learning_pace       TEXT,                     -- 학습 페이스 메모
  notes               TEXT,
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ── chat_history (대화 이력 계정화; localStorage 대체) ──────────────
CREATE TABLE IF NOT EXISTS chat_history (
  user_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  collection TEXT NOT NULL,                     -- 'concepts' | 'problems'
  slug       TEXT NOT NULL,
  messages   JSONB NOT NULL DEFAULT '[]',
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (user_id, collection, slug)
);

-- ── auth_throttle (로그인 브루트포스 방어) ─────────────────────────
CREATE TABLE IF NOT EXISTS auth_throttle (
  key           TEXT PRIMARY KEY,               -- 'login:'||lower(email) 또는 'ip:'||ip
  fail_count    INT NOT NULL DEFAULT 0,
  first_fail_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  locked_until  TIMESTAMPTZ
);

-- problem_state/attempts → users FK (legacy 행 존재해 이제 유효). 멱등 위해 drop-if-exists.
ALTER TABLE problem_state    DROP CONSTRAINT IF EXISTS problem_state_user_fk;
ALTER TABLE problem_state    ADD  CONSTRAINT problem_state_user_fk
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
ALTER TABLE problem_attempts DROP CONSTRAINT IF EXISTS problem_attempts_user_fk;
ALTER TABLE problem_attempts ADD  CONSTRAINT problem_attempts_user_fk
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

COMMIT;
