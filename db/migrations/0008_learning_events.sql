-- ── learning_events (학습 상태 변경의 정본) ───────────────────────────────────
--
-- ★왜: 지금 `reset`·`mark-mastered`·`skip` 은 **파생 상태(problem_state)를 직접 고친다.**
--   `reset` 은 아예 DELETE 다. 그래서 problem_attempts 로부터 상태를 재계산하는 순간
--   **지운 상태가 되살아나고**(시도 기록은 남아 있으니까) **mark-mastered·skip 은 사라진다**
--   (재계산 규칙에 그런 입력이 없으니까). 재계산을 도입하기 **전에** 이걸 먼저 해야 한다.
--
--   같은 이유로 개념 숙련도 evidence(concept_mastery.mastery_evidence)도 여기 남긴다 —
--   그건 시도 기록에서 유도되는 값이 아니라 **판단의 산물**이라 재계산으로 복원되지 않는다.
--
-- 설계
--   - **append-only.** 이 테이블은 고치지 않는다. 취소도 "취소 이벤트" 로 적는다.
--   - `seq` 는 서버가 매기는 단조 증가값 — Phase 4 의 **커서 기반 델타 동기화**가 그대로 쓴다.
--     (기기 시계는 못 믿는다. 오프라인 기기의 시계가 틀어져도 seq 는 서버 도착순으로 정렬된다)
--   - `occurred_at`(기기에서 일어난 시각) 과 `recorded_at`(서버 수신 시각)을 **나눈다.**
--     오프라인 기기가 3일 뒤에 합류하면 둘이 크게 벌어진다. **재계산 순서는 occurred_at**,
--     **동기화 커서는 seq** — 이 둘을 하나로 합치면 둘 중 하나가 반드시 틀린다.
--   - `event_id` 는 클라이언트가 만든다(멱등키). 오프라인 큐가 같은 이벤트를 두 번 올려도
--     `(user_id, event_id)` 유니크로 한 번만 남는다. 네트워크 재시도는 정상 상황이지
--     예외가 아니다.
CREATE TABLE IF NOT EXISTS learning_events (
  seq         BIGSERIAL PRIMARY KEY,
  event_id    UUID NOT NULL DEFAULT gen_random_uuid(),
  user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  kind        TEXT NOT NULL,
  target      TEXT NOT NULL,                       -- 문제 slug 또는 개념 slug
  payload     JSONB NOT NULL DEFAULT '{}',
  occurred_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),  -- 기기에서 일어난 시각(재계산 순서)
  recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),  -- 서버 수신 시각
  UNIQUE (user_id, event_id)
);

-- 델타 동기화: "내 커서 이후 것 주세요" 가 이 인덱스 하나로 끝난다.
CREATE INDEX IF NOT EXISTS learning_events_user_seq_idx ON learning_events (user_id, seq);
-- 재계산: 대상별로 시간순 재생.
CREATE INDEX IF NOT EXISTS learning_events_target_idx ON learning_events (user_id, target, occurred_at);
