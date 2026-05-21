-- 0002: Add `grade` column to exams + extend UNIQUE constraint.
-- Lets us distinguish 학평/모의고사 by 학년 (고1/고2/고3) and 검정고시 by 중졸/고졸,
-- which would otherwise collide on (agency, exam_type, year, session).

BEGIN;

ALTER TABLE exams ADD COLUMN IF NOT EXISTS grade TEXT;
COMMENT ON COLUMN exams.grade IS '고1/고2/고3 (모의고사·학력평가), 중졸/고졸 (검정고시), NULL (수능·모의평가)';

ALTER TABLE exams DROP CONSTRAINT IF EXISTS exams_agency_exam_type_year_session_key;
ALTER TABLE exams DROP CONSTRAINT IF EXISTS exams_unique;
ALTER TABLE exams ADD CONSTRAINT exams_unique
  UNIQUE (agency, exam_type, year, session, grade);

COMMIT;
