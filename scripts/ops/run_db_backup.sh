#!/bin/bash
# math-study 프로덕션 DB 백업 — 야간 pg_dump -Fc + 원격 1부 + 30일 로테이션.
#
# ★왜 필요했나(2026-08-13 리뷰에서 발견): 유료 구독자를 받으려는 시점에 **백업이 0개**였다.
#   진도·필기·대화가 도커 볼륨 ms_pgdata 하나에만 있었고, 서버에 돌던 백업 크론 2건은
#   `-d legal_brain_db` 고정이라(포렌식 전용) math-study 는 대상이 아니었다.
#   되돌릴 수 없는 유일한 종류의 사고라 최우선으로 넣는다.
#
# 설계
#   - DB 는 컨테이너 안에 있고 호스트 포트가 없다 → `docker compose exec -T db pg_dump`.
#   - `.partial` 로 받고 성공 시에만 rename(원자적). 실패 시 부분 파일을 남기지 않는다.
#   - **덤프를 만든 뒤 pg_restore -l 로 읽어본다** — 0바이트/깨진 덤프를 "성공"으로 세지 않기 위해.
#   - 원격 미도달이면 로컬 백업은 남기되 exit 1(크론 로그에 실패로 남게).
#
# ⚠️ 앞으로의 함정: 사용자 데이터가 **DB 와 R2 로 쪼개지면**(Phase 5) 이 스크립트만으로 불충분하다.
#    필기·이미지 본문이 R2 로 나가는 순간, **DB 와 R2 를 같은 시점으로 묶어야** 한다 —
#    한쪽만 복구하면 참조가 깨진 반쪽 데이터가 된다.
#
# 사용: run_db_backup.sh            (크론)
#       run_db_backup.sh --verify   (최신 백업을 빈 DB 에 복원해 확인 — 복구 리허설)
set -o pipefail

REPO=/home/insung/math-study
LOCAL_DIR="$HOME/backups/math-study"          # ★레포 밖 — 커밋 사고 방지
REMOTE="tme-laptop"
RDIR="/mnt/webdav/Cloud/db_backup/math-study"
KEEP_DAYS=30
LOG="$HOME/backups/math-study/backup.log"
SSH="ssh -o ConnectTimeout=20 -o BatchMode=yes -o ServerAliveInterval=30"
STAMP="$(date +%Y%m%d_%H%M)"
FILE="mathstudy_${STAMP}.dump"

mkdir -p "$LOCAL_DIR"
log(){ echo "$(date '+%F %T %Z') $*" | tee -a "$LOG"; }

# ── 복구 리허설 ────────────────────────────────────────────────────────────────
# 백업이 "있다"와 "복구된다"는 다른 말이다. 임시 DB 에 실제로 복원해 본다.
if [ "${1:-}" = "--verify" ]; then
  LATEST="$(ls -t "$LOCAL_DIR"/mathstudy_*.dump 2>/dev/null | head -1)"
  [ -z "$LATEST" ] && { log "[VERIFY] 백업 파일이 없다"; exit 1; }
  log "[VERIFY] 대상 $LATEST ($(du -h "$LATEST" | cut -f1))"
  TMPDB="ms_restore_test_$$"
  docker exec deploy-db-1 psql -U mathstudy -d postgres -c "DROP DATABASE IF EXISTS $TMPDB;" >/dev/null 2>&1
  docker exec deploy-db-1 psql -U mathstudy -d postgres -c "CREATE DATABASE $TMPDB;" >/dev/null || { log "[VERIFY] 임시 DB 생성 실패"; exit 1; }
  if docker exec -i deploy-db-1 pg_restore -U mathstudy -d "$TMPDB" --no-owner --no-privileges < "$LATEST" >/dev/null 2>&1; then
    # 핵심 테이블이 실제로 살아났는지 — 행 수까지 확인
    OUT=$(docker exec deploy-db-1 psql -U mathstudy -d "$TMPDB" -t -A -F'|' -c \
      "SELECT (SELECT count(*) FROM users), (SELECT count(*) FROM problems), (SELECT count(*) FROM chat_history), (SELECT count(*) FROM handwriting);" 2>&1)
    log "[VERIFY] ✅ 복원 성공 — users|problems|chat_history|handwriting = $OUT"
    RC=0
  else
    log "[VERIFY] ❌ 복원 실패"; RC=1
  fi
  docker exec deploy-db-1 psql -U mathstudy -d postgres -c "DROP DATABASE IF EXISTS $TMPDB;" >/dev/null 2>&1
  exit $RC
fi

# ── 덤프 ──────────────────────────────────────────────────────────────────────
cd "$REPO/deploy" || { log "[FATAL] deploy 디렉터리 없음"; exit 1; }
if ! docker compose exec -T db pg_dump -U mathstudy -Fc mathstudy > "$LOCAL_DIR/$FILE.partial" 2>>"$LOG"; then
  log "[FATAL] pg_dump 실패"; rm -f "$LOCAL_DIR/$FILE.partial"; exit 1
fi

# ★만들자마자 읽어본다 — 0바이트·깨진 덤프를 성공으로 세지 않기 위해.
if ! pg_restore -l "$LOCAL_DIR/$FILE.partial" >/dev/null 2>&1; then
  # 호스트에 pg_restore 가 없으면 컨테이너로 검사
  if ! docker exec -i deploy-db-1 pg_restore -l < "$LOCAL_DIR/$FILE.partial" >/dev/null 2>&1; then
    log "[FATAL] 덤프가 읽히지 않는다 — 폐기"; rm -f "$LOCAL_DIR/$FILE.partial"; exit 1
  fi
fi
mv "$LOCAL_DIR/$FILE.partial" "$LOCAL_DIR/$FILE"
SZ=$(du -h "$LOCAL_DIR/$FILE" | cut -f1)
log "[LOCAL] $FILE ($SZ)"

# ── 원격 1부 ──────────────────────────────────────────────────────────────────
if $SSH "$REMOTE" true 2>/dev/null; then
  $SSH "$REMOTE" "mkdir -p '$RDIR'" 2>/dev/null
  if scp -o ConnectTimeout=20 -o BatchMode=yes -q "$LOCAL_DIR/$FILE" "$REMOTE:$RDIR/$FILE.partial" 2>>"$LOG" \
     && $SSH "$REMOTE" "mv '$RDIR/$FILE.partial' '$RDIR/$FILE'" 2>>"$LOG"; then
    log "[REMOTE] $REMOTE:$RDIR/$FILE"
    $SSH "$REMOTE" "find '$RDIR' -name 'mathstudy_*.dump' -mtime +$KEEP_DAYS -delete" 2>/dev/null
  else
    log "[WARN] 원격 전송 실패 — 로컬본은 있음"; REMOTE_FAIL=1
  fi
else
  log "[WARN] $REMOTE 미도달 — 로컬본만 있음"; REMOTE_FAIL=1
fi

# ── 로테이션 ──────────────────────────────────────────────────────────────────
find "$LOCAL_DIR" -name 'mathstudy_*.dump' -mtime +$KEEP_DAYS -delete
N=$(ls -1 "$LOCAL_DIR"/mathstudy_*.dump 2>/dev/null | wc -l)
log "[DONE] 보관 ${N}개 (로컬 ${KEEP_DAYS}일)"

# 로그 무한증식 방지
tail -3000 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"

exit ${REMOTE_FAIL:-0}
