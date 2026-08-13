-- ── 필기 문서에 서버 부여 순번(seq) ──────────────────────────────────────────
--
-- ★왜 시각이 아니라 순번인가: 기기 시계는 못 믿는다. 아이패드와 노트북의 시계가 몇 초만
--   어긋나도 "누가 더 최신인가" 가 뒤집힌다. 서버가 매기는 단조 증가값은 그런 일이 없다.
--   [[learning_events]] 의 seq 와 같은 이유·같은 방식이다.
--
-- ★무엇에 쓰나: "내 커서 이후에 바뀐 문서만 주세요" 라는 델타 동기화. 필기는 문서 하나가
--   수십 KB 라, 페이지를 열 때마다 전부 받으면 앱에서 못 쓴다.
--
-- ⚠️ 이 값은 **문서의 버전이 아니라 서버 도착 순서**다. 충돌 해소에 쓰면 안 된다 —
--    합치기는 스트로크 id 합집합에서 묘비를 빼는 방식(v3)이고, seq 는 "무엇을 받을지" 만 정한다.
CREATE SEQUENCE IF NOT EXISTS handwriting_seq;

ALTER TABLE handwriting ADD COLUMN IF NOT EXISTS seq BIGINT;

-- 기존 행에도 값을 채운다(updated_at 순서대로 — 도착 순서의 최선 근사).
UPDATE handwriting SET seq = nextval('handwriting_seq') WHERE seq IS NULL;

-- "이 사용자의 커서 이후" 조회가 이 인덱스 하나로 끝난다.
CREATE INDEX IF NOT EXISTS handwriting_user_seq_idx ON handwriting (user_id, seq);
