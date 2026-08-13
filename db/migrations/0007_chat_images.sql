-- ── chat_images (대화 첨부 이미지를 jsonb 밖으로) ─────────────────────────────
--
-- ★왜: chat_history.messages 는 매 턴마다 **배열 전체가 통째로 재기록**된다. 이미지가
--   dataURL 로 그 안에 있으면 대화 1건이 568KB 였고, 한 턴 주고받을 때마다 그 568KB 를
--   다시 쓴다. 첨부가 쌓일수록 턴당 쓰기 비용이 선형으로 는다.
--
-- ★왜 그냥 "안 저장" 이 아니라 "빼내기" 인가: 2026-08-13 실측에서 512px 표시본은 판독
--   오류 10건, 1568px 타일은 1건이었다. 다음 턴 이미지 창이 표시본으로 갈음될 수 없으므로
--   **타일은 반드시 영속해야 한다.** 남은 선택지는 "어디에 두느냐" 뿐이다.
--
-- 설계: 내용주소(sha256). messages 에는 'img:sha256:<hex>' 참조만 남는다.
--   - 같은 이미지가 여러 메시지·여러 대화에 나와도 **본문은 1부**
--   - 나중에 R2 로 옮길 때 **참조 형식은 그대로**, 해석 계층의 백엔드만 갈아끼운다
--     (그게 이 마이그레이션의 본체다 — bytea 는 임시 백엔드일 뿐)
--
-- ⚠️ 지금 DB 안에 두는 이유: 백업이 DB 하나만 보면 되기 때문(scripts/ops/run_db_backup.sh).
--    R2 로 나가는 순간 **DB 와 R2 를 같은 시점으로 묶어야** 반쪽 복구가 안 난다.
CREATE TABLE IF NOT EXISTS chat_images (
  hash       TEXT PRIMARY KEY,            -- sha256 hex (참조는 'img:sha256:<hash>')
  mime       TEXT NOT NULL,
  data       BYTEA NOT NULL,
  bytes      INT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 고아 정리(회원 탈퇴·대화 삭제 후)용 — 참조가 messages 안 문자열이라 FK 를 못 건다.
CREATE INDEX IF NOT EXISTS chat_images_created_idx ON chat_images (created_at);
