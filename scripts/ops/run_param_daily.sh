#!/usr/bin/env bash
# ============================================================================
# 솔버 파라미터화 — 일일 소넷 드립 (크론 07:00)
#
#   scripts/ops/run_param_daily.sh              # 기본: 소넷 · 워커 8 · 2시간 박스
#   MAX_SECONDS=14400 scripts/ops/run_param_daily.sh    # 버스트(4시간)
#   WORKERS=12 MAX_SECONDS=21600 scripts/ops/run_param_daily.sh
#
# ★왜 소넷인가: 구독 쿼터라 **한계비용이 0** 이다. Hermes/DeepSeek 경로는 통과율이
#   더 좋지만(83% vs …) 건당 $0.03 로 실제 돈이 나간다 — 전수 4,098건이면 $124.
#   그래서 평시는 소넷으로 조금씩 갉고, 여유가 있다고 판단되면 MAX_SECONDS 를 늘려
#   버스트한다. DeepSeek 은 쿼터가 말랐을 때의 예비 경로다.
#
# ★왜 건수가 아니라 시간 박스인가: 문제 난이도가 들쭉날쭉해 건수로 묶으면 어떤 날은
#   30분, 어떤 날은 4시간이 된다. 쿼터 소모를 예측 가능하게 하려면 시간으로 묶어야 한다.
#
# 안전장치(배치 본체가 제공):
#   · 죽은 자리에서 재개 — db/solutions/_paramstate.json
#   · 두 게이트를 통과한 결과만 채택, 실패하면 원본 복구(개악 없음)
#   · 쿼터 소진·인증 만료 감지 시 즉시 중단(남은 건이 전부 실패로 기록되는 것을 막는다)
#   · 연속 6건 실패 시 회로차단
# ============================================================================
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO" || exit 1

MODEL="${MODEL:-sonnet}"
WORKERS="${WORKERS:-8}"
MAX_SECONDS="${MAX_SECONDS:-7200}"          # 기본 2시간
LOCK="/tmp/math-study-param-daily.lock"
LOG_DIR="${PARAM_LOG_DIR:-/tmp/ingest_logs}"   # ★/progress 가 읽는 디렉터리
LOG="$LOG_DIR/param_daily_$(date +%Y%m%d_%H%M%S).log"
mkdir -p "$LOG_DIR"

# ── 겹침 방지: 어제 것이 아직 돌고 있으면 오늘은 건너뛴다 ────────────────────
exec 9>"$LOCK"
if ! flock -n 9; then
  echo "[$(date '+%F %T')] 이전 실행이 아직 돌고 있다 — 건너뜀" | tee -a "$LOG"
  exit 0
fi

echo "[$(date '+%F %T')] 시작 — 모델 $MODEL · 워커 $WORKERS · 시간박스 ${MAX_SECONDS}s" | tee -a "$LOG"

python3 scripts/parameterize_solvers.py \
  --model "$MODEL" --workers "$WORKERS" \
  --max-seconds "$MAX_SECONDS" --log "$LOG" >>"$LOG" 2>&1
RC=$?

# ── 결과 커밋 ───────────────────────────────────────────────────────────────
# ★반드시 스스로 커밋한다. 스테이징만 해두고 두면 03:00 widget_spec_loop 크론의
#   `git commit`(경로 미지정)이 남의 변경까지 같이 가져간다. add 도 경로를 좁힌다.
git add -- db/solutions 2>/dev/null
if git diff --cached --quiet -- db/solutions; then
  echo "[$(date '+%F %T')] 변경 없음 — 커밋 생략 (rc=$RC)" | tee -a "$LOG"
else
  N=$(git diff --cached --name-only -- db/solutions | grep -c '\.py$')
  git commit -q -m "feat(solver): 파라미터화 일일 배치 — ${N}건 ($MODEL)

$(date '+%F') 07:00 크론. 시간박스 ${MAX_SECONDS}s · 워커 ${WORKERS}.
두 게이트 통과분만 채택(실패분은 원본 그대로). 로그: $LOG" \
    && echo "[$(date '+%F %T')] 커밋 ${N}건" | tee -a "$LOG"
  git pull --rebase -q && git push -q --no-verify \
    && echo "[$(date '+%F %T')] 푸시 완료" | tee -a "$LOG" \
    || echo "[$(date '+%F %T')] ⚠ 푸시 실패 — 커밋은 남아 있다" | tee -a "$LOG"
fi

echo "[$(date '+%F %T')] 종료 rc=$RC" | tee -a "$LOG"
exit "$RC"
