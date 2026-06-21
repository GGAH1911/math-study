#!/usr/bin/env bash
# agy(Gemini "3.5 Flash (Medium)") 리프레시 사이클 keepalive.
#   목적: 사용 안 해도 주기적으로 트리비얼 쿼리("1+1")를 던져 리프레시 사이클을 계속 돌림
#         → 파이프라인이 agy 재교정에 쓸 때 항상 쿼터가 살아있게.
#   파이프라인(corrector)이 agy를 활발히 쓸 때는 그 사용 자체가 keepalive지만,
#   유휴(밤·세션 종료) 시 사이클이 멈출 수 있어 이 크론이 보강한다.
#   ★agy는 단일 인스턴스 — 파이프라인 agy 재교정과 동시 호출 시 충돌("백그라운드 태스크 대기").
#     timeout 으로 빠지며, 그 경우엔 파이프라인 사용이 이미 사이클을 유지하므로 무해.
# crontab(매 4시간, ~5h 윈도우 내 항상 최근 ping):  0 */4 * * * /home/insung/Projects/math-study/web/scripts/agy_keepalive.sh
set -u
AGY=/home/insung/.local/bin/agy
LOG=/tmp/ingest_logs/agy_keepalive.log
mkdir -p /tmp/ingest_logs
TS=$(date '+%Y-%m-%d %H:%M:%S')
OUT=$(timeout 120 "$AGY" -p "1+1은? 숫자만 답하라." --model "Gemini 3.5 Flash (Medium)" 2>&1 | tr '\n' ' ' | sed 's/  */ /g' | head -c 160)
[ -z "${OUT// }" ] && OUT="(빈응답 — 쿼터소진/충돌, 다음 사이클 재시도)"
echo "[$TS] ping→ $OUT" >> "$LOG"
