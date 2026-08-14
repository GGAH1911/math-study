#!/usr/bin/env bash
# ============================================================================
# 솔버 파라미터화 — 일일 소넷 드립 (크론 07:00)
#
#   scripts/ops/run_param_daily.sh              # 기본: 소넷 · 워커 8 · 2시간 박스
#   MAX_SECONDS=14400 scripts/ops/run_param_daily.sh    # 버스트(4시간)
#   WORKERS=12 MAX_SECONDS=21600 scripts/ops/run_param_daily.sh
#
# ★왜 소넷인가: 구독 쿼터라 **한계비용이 0** 이다. Hermes/DeepSeek 은 통과율이 더 좋아도
#   **Nous Portal 이 종량제라**(2026-08-14 확인) 건당 $0.03 이 진짜 나간다 — 잔여
#   4,049건이면 약 $122.
#   ⚠️ `~/.hermes/state.db` 의 `actual_cost_usd` 가 0 인 것은 **공짜라는 뜻이 아니라**
#      provider 가 실비를 안 돌려준다는 뜻이다. 판단은 `estimated_cost_usd` 로 한다.
#   그래서 버스트는 **MODEL 을 바꾸는 게 아니라 MAX_SECONDS 를 늘리는 것**이다
#   (소넷 그대로 → 추가 지출 0). DeepSeek 을 꺼낼 자리는 하나뿐 — 소넷 쿼터가 말랐는데
#   그날 안에 꼭 진도를 빼야 할 때. 급하지 않으면 다음 07:00 을 기다리는 게 싸다($0).
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
  # ★`-z` 필수. 한글 파일명은 git 이 "db/solutions/2019_\352\263\240..._25.py" 처럼
  #   **이스케이프해 따옴표로 감싼다** → 줄 끝이 `y` 가 아니라 `"` 라 `grep '\.py$'` 가
  #   전부 빗나가 건수가 늘 0 으로 찍혔다(2026-08-14 실측). -z 는 인용을 아예 끈다.
  N=$(git diff --cached --name-only -z -- db/solutions | tr '\0' '\n' | grep -c '\.py$')
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
