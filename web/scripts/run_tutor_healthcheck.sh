#!/bin/bash
# 튜터 딥 헬스체크 크론 (시간당 1회).
#   /api/health?deep=1 은 튜터 백엔드를 **실제로 호출**한다. 얕은 헬스(DB만)는 2026-08-12 사고 때
#   15시간 내내 200 이었는데 정작 튜터는 죽어 있었다 — 그래서 별도 경로로 주기 점검한다.
#   과금은 호출당 $0.00001 수준(최소 프롬프트·max_tokens 8) → 월 $0.01 미만.
#
# 실패 시: 로그에 남기고, 연속 실패면 눈에 띄게 표시. (알림 채널은 추후 — 우선 기록부터.)
set -uo pipefail
LOG=/tmp/tutor_health.log
STATE=/tmp/tutor_health.state
URL="http://127.0.0.1:${MS_WEB_PORT:-4324}/api/health?deep=1"
TS=$(date -Is)

BODY=$(curl -s --max-time 60 -w '\n%{http_code}' "$URL" 2>&1)
CODE=$(printf '%s' "$BODY" | tail -1)
JSON=$(printf '%s' "$BODY" | head -n -1)

FAILS=$(cat "$STATE" 2>/dev/null || echo 0)
if [ "$CODE" = "200" ]; then
  [ "$FAILS" -gt 0 ] && echo "$TS 복구됨 (연속실패 $FAILS 회 후) $JSON" >> "$LOG"
  echo 0 > "$STATE"
  echo "$TS ok $JSON" >> "$LOG"
else
  FAILS=$((FAILS + 1))
  echo "$FAILS" > "$STATE"
  echo "$TS ★실패($FAILS회 연속) HTTP=$CODE $JSON" >> "$LOG"
  # 3회 연속(=3시간)이면 확실한 장애 — 로그에 크게 남긴다.
  [ "$FAILS" -ge 3 ] && echo "$TS ██ 튜터 3시간 연속 불통 — 확인 필요 ██" >> "$LOG"
fi

# 로그 무한증식 방지(최근 2000줄 유지).
[ -f "$LOG" ] && tail -2000 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
