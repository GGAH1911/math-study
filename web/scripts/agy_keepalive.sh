#!/usr/bin/env bash
# agy(Gemini "3.5 Flash (Medium)") 리프레시 사이클 keepalive 데몬.
#   목적: 사용 안 해도 주기적 트리비얼 쿼리("1+1")로 리프레시 사이클을 계속 돌림
#         → 파이프라인 재교정용 agy 쿼터를 항상 살려둠.
#   ★간격 = 5시간 1분(18060s): 리프레시 5h 직후(+1분 여유)에 ping → 새 윈도우 시작.
#     딱 5h면 리프레시 경계와 레이스라 위험 → 1분 마진(사용자 지정).
#   ★cron은 5h1m 불가(301분, 분 필드 0-59 초과) → 데몬 루프(sleep 18060).
#   ★agy 단일 인스턴스 — 파이프라인 agy 재교정과 동시 호출 시 빈응답(충돌). 그땐 파이프라인 사용이
#     이미 사이클을 유지하므로 무해. 일시 충돌 대비 짧은 재시도 3회.
#   launch: setsid bash web/scripts/agy_keepalive.sh </dev/null >/dev/null 2>&1 &   (flock가 중복 차단)
#   reboot 생존: crontab @reboot 항목이 재기동.
set -u
exec 9>/tmp/agy_keepalive.lock
flock -n 9 || { echo "이미 실행 중 — 중복 기동 안 함"; exit 0; }   # 단일 인스턴스
AGY=/home/insung/.local/bin/agy
LOG=/tmp/ingest_logs/agy_keepalive.log
mkdir -p /tmp/ingest_logs
ping_agy() {
  local i out
  for i in 1 2 3; do
    out=$(timeout 120 "$AGY" -p "1+1은? 숫자만 답하라." --model "Gemini 3.5 Flash (Medium)" 2>&1 | tr '\n' ' ' | sed 's/  */ /g' | head -c 160)
    [ -n "${out// }" ] && { printf '%s' "$out"; return; }
    sleep 30   # 일시 충돌(파이프라인 agy) 대비 짧은 재시도
  done
  printf '(빈응답 3회 — 쿼터소진/충돌, 다음 사이클 재시도)'
}
echo "[$(date '+%Y-%m-%d %H:%M:%S')] === keepalive 데몬 시작 (간격 5h1m=18060s) ===" >> "$LOG"
while true; do
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ping→ $(ping_agy)" >> "$LOG"
  sleep 18060   # 5시간 1분
done
