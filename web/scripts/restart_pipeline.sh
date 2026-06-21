#!/usr/bin/env bash
# 파이프라인 재시작 — 기존 kill + gemma 검증 config로 시작.
#   ★자가매칭 회피: 이 로직을 스크립트 파일에 두면 호출 셸 cmdline은 'bash restart_pipeline.sh'뿐이라
#     kill grep이 호출 셸을 안 잡는다(inline 명령에 'correct_verify_pipeline' 박으면 자기를 죽임).
#   config: GEMMA_PAR=1(1차) + PAR_V=1(검증) = gemma 2동시(하나 교정·하나 검증) + VERIFY_MODEL=gemma(로컬 무료) + NO_RECORRECT(재교정은 별도 agy 러너).
cd /home/insung/Projects/math-study/web
ps aux | grep '[c]orrect_verify_pipeline' | awk '{print $2}' | xargs -r kill -9 2>/dev/null
sleep 4
: > /tmp/ingest_logs/verify_usage.log
TS=$(date +%s)
LOG="/tmp/ingest_logs/pipe_${TS}.log"
echo "$LOG" > /tmp/pipeline_log.txt
setsid env RUN_TS=$TS DUAL=1 GEMMA_PAR=1 PAR_V=1 NO_RECORRECT=1 VERIFY_MODEL=gemma CORRECT_BACKEND=gemma node scripts/correct_verify_pipeline.mjs > "$LOG" 2>&1 < /dev/null &
disown
echo "restarted: GEMMA_PAR=1 PAR_V=1 VERIFY_MODEL=gemma LOG=$LOG"
