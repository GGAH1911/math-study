#!/usr/bin/env bash
# 파이프라인 재시작 — 기존 kill + gemma 검증 config로 시작.
#   ★자가매칭 회피: 이 로직을 스크립트 파일에 두면 호출 셸 cmdline은 'bash restart_pipeline.sh'뿐이라
#     kill grep이 호출 셸을 안 잡는다(inline 명령에 'correct_verify_pipeline' 박으면 자기를 죽임).
#   config: GEMMA_PAR=1(1차) + PAR_V=1(검증) = gemma 2동시(하나 교정·하나 검증) + VERIFY_MODEL=gemma(로컬 무료) + NO_RECORRECT(재교정은 별도 agy 러너).
#   ★config 주의: gemma 는 사장님 맥북 mlx 서버가 떠 있어야 하고 agy 는 현재 사용 불가다.
#     둘 다 없으면 CORRECT_BACKEND=sonnet 으로 바꿔 쓴다.
# ★스크립트 위치 기준(이동 내성) + cd 실패 시 반드시 중단. 예전엔 옛 머신 경로를 `|| exit`
#   없이 cd 해서, 레포 이전 후 cd 가 실패해도 계속 진행했다 → **돌던 파이프라인을 죽이기만
#   하고 재시작에 실패한 뒤 "restarted:" 를 찍어** 성공한 것처럼 보였다(2026-08-15 감사).
#   죽이기 전에 자리부터 확인한다 — 되살릴 수 없으면 아예 죽이지 않는다.
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)" || { echo "✗ web/ 이동 실패 — 중단"; exit 1; }
[ -f scripts/correct_verify_pipeline.mjs ] || { echo "✗ correct_verify_pipeline.mjs 없음 — 죽이지 않고 중단"; exit 1; }
ps aux | grep '[c]orrect_verify_pipeline' | awk '{print $2}' | xargs -r kill -9 2>/dev/null
sleep 4
: > /tmp/ingest_logs/verify_usage.log
TS=$(date +%s)
LOG="/tmp/ingest_logs/pipe_${TS}.log"
echo "$LOG" > /tmp/pipeline_log.txt
setsid env RUN_TS=$TS DUAL=1 GEMMA_PAR=1 PAR_V=1 NO_RECORRECT=1 VERIFY_MODEL=gemma CORRECT_BACKEND=gemma node scripts/correct_verify_pipeline.mjs > "$LOG" 2>&1 < /dev/null &
disown
echo "restarted: GEMMA_PAR=1 PAR_V=1 VERIFY_MODEL=gemma LOG=$LOG"
