-- Math Study — initial schema (Plan §3, Tier 1+2 + 사용자별 Tier 3)
-- 4-Tier SSOT (D10): markdown frontmatter ↔ DB 단방향 sync (frontmatter가 metadata SSOT,
-- DB는 빠른 쿼리·통계·사용자 상태 SSOT)

BEGIN;

CREATE EXTENSION IF NOT EXISTS "pgcrypto";  -- gen_random_uuid()

-- ───────────────────────────────────────────────────────────────────
-- exams: 시험 회차 (수능·모의평가·학력평가 단위)
-- ───────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS exams (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agency      TEXT NOT NULL,                -- 평가원 / 교육청(시도명) / 자체-진단
  exam_type   TEXT NOT NULL,                -- 수능 / 모의평가 / 학력평가 / 진단
  year        INT  NOT NULL,                -- 학년도
  session     TEXT,                         -- 11월 본수능 / 6월 / 9월 / 3월 / 4월 / 7월 / 10월
  source_pdf  TEXT,                         -- 원본 PDF 상대 경로
  ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (agency, exam_type, year, session)
);

COMMENT ON TABLE exams IS 'Korean math exam session (수능/모의평가/학력평가). One row per (agency, exam_type, year, session).';

-- ───────────────────────────────────────────────────────────────────
-- problems: 개별 문항 (Tier 1 + Tier 2)
-- ───────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS problems (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  exam_id               UUID NOT NULL REFERENCES exams(id) ON DELETE CASCADE,
  subject               TEXT NOT NULL,           -- 공통 / 미적분 / 확률과통계 / 기하 / 중1 등
  number                INT  NOT NULL,           -- 문항 번호
  score                 INT,                     -- 배점 (2/3/4)
  format                TEXT,                    -- choice / numeric / descriptive
  text_markdown         TEXT NOT NULL,           -- KaTeX 포함 본문
  has_image             BOOLEAN NOT NULL DEFAULT FALSE,
  image_paths           TEXT[] DEFAULT '{}',
  answer                TEXT,                    -- 객관식: '1'-'5' / 단답형: 수치
  official_pass_rate    REAL,                    -- KICE 발표 정답률 %
  official_solution_url TEXT,                    -- EBSi/평가원 해설
  -- Tier 2 (LLM-derived)
  unit_slug             TEXT,                    -- wiki concept slug (1개)
  exam_intent           TEXT,                    -- 한 줄 출제 의도
  killer_tier           TEXT,                    -- early / mid / high / killer
  cognitive_type        TEXT,                    -- 계산 / 개념 / 응용 / 추론 / 통합
  expected_time_sec     INT,
  -- frontmatter ↔ DB 동기화 위한 경로
  frontmatter_path      TEXT,                    -- docs/problems/<slug>.md
  UNIQUE (exam_id, subject, number),
  CHECK (format IS NULL OR format IN ('choice', 'numeric', 'descriptive')),
  CHECK (killer_tier IS NULL OR killer_tier IN ('early', 'mid', 'high', 'killer')),
  CHECK (cognitive_type IS NULL OR cognitive_type IN ('계산', '개념', '응용', '추론', '통합'))
);

COMMENT ON TABLE problems IS 'Tier 1 (PDF/KICE-extracted) + Tier 2 (LLM-mapped) problem metadata. text_markdown is the rendered Korean problem with KaTeX.';

-- ───────────────────────────────────────────────────────────────────
-- problem_concepts: 문항 ↔ wiki concept 다대다 매핑
-- ───────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS problem_concepts (
  problem_id    UUID NOT NULL REFERENCES problems(id) ON DELETE CASCADE,
  concept_slug  TEXT NOT NULL,                  -- wiki concept page stem
  weight        REAL NOT NULL DEFAULT 1.0,      -- 매핑 강도 (LLM confidence)
  is_primary    BOOLEAN NOT NULL DEFAULT FALSE, -- TRUE: 이 문제의 주된 unit / FALSE: 부수적 spoke
  PRIMARY KEY (problem_id, concept_slug)
);

COMMENT ON TABLE problem_concepts IS 'Maps a problem to its primary unit + 1-3 spoke concepts (definition/theorem/example).';

-- ───────────────────────────────────────────────────────────────────
-- problem_state: 사용자별 학습 상태 (Tier 3, DB가 SSOT)
-- ───────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS problem_state (
  user_id         UUID NOT NULL,                -- 단일 사용자 시 default UUID
  problem_id      UUID NOT NULL REFERENCES problems(id) ON DELETE CASCADE,
  status          TEXT NOT NULL DEFAULT 'unsolved',  -- unsolved / solved / review
  review_state    TEXT NOT NULL DEFAULT 'new',       -- new / learning / mature
  next_review     DATE,
  last_attempted  TIMESTAMPTZ,
  attempt_count   INT NOT NULL DEFAULT 0,
  PRIMARY KEY (user_id, problem_id),
  CHECK (status IN ('unsolved', 'solved', 'review')),
  CHECK (review_state IN ('new', 'learning', 'mature'))
);

-- ───────────────────────────────────────────────────────────────────
-- problem_attempts: 풀이 시도 이력 (분석·학습 패턴용)
-- ───────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS problem_attempts (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id         UUID NOT NULL,
  problem_id      UUID NOT NULL REFERENCES problems(id) ON DELETE CASCADE,
  attempted_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  answer_given    TEXT,
  is_correct      BOOLEAN,
  time_taken_sec  INT,
  notes           TEXT
);

-- ───────────────────────────────────────────────────────────────────
-- Indexes
-- ───────────────────────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_problems_unit       ON problems(unit_slug);
CREATE INDEX IF NOT EXISTS idx_problems_killer     ON problems(killer_tier);
CREATE INDEX IF NOT EXISTS idx_problems_exam       ON problems(exam_id);
CREATE INDEX IF NOT EXISTS idx_pc_concept          ON problem_concepts(concept_slug);
CREATE INDEX IF NOT EXISTS idx_state_review        ON problem_state(user_id, next_review);
CREATE INDEX IF NOT EXISTS idx_attempts_user       ON problem_attempts(user_id, attempted_at DESC);

COMMIT;
