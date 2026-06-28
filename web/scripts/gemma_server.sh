#!/usr/bin/env bash
# 맥북 Pro mlx_vlm gemma 서버 관리 — corrector(비전 교정)·개념 본문 변환이 의존.
# 상세 운영 지침: docs/ops/runbooks/GEMMA_SERVER.md
#
#   ./gemma_server.sh start     기동(분리·모델 로딩 대기)
#   ./gemma_server.sh status    생사 확인
#   ./gemma_server.sh stop      종료
#   ./gemma_server.sh restart   재시작
#   ./gemma_server.sh watch     watchdog(60s마다 점검, 죽으면 자동 재시작) — 긴 배치 중 권장
#   ./gemma_server.sh test      실제 생성 1회 확인
set -uo pipefail

HOST="${GEMMA_SSH:-macbook}"                                  # tailscale: macbook-pro 100.79.230.49
URL="http://100.79.230.49:8080/v1"
MODEL="mlx-community/gemma-4-26B-A4B-it-qat-4bit"
RDIR="~/gemma-corrector"                                      # 원격 작업 디렉터리(venv·server.log)
RPY=".venv/bin/python"

up() { curl -s -o /dev/null --max-time 8 "$URL/models" 2>/dev/null; }

case "${1:-status}" in
  start)
    if up; then echo "이미 실행 중"; exit 0; fi
    ssh "$HOST" "cd $RDIR && nohup $RPY -m mlx_vlm.server --model $MODEL --port 8080 --host 0.0.0.0 > server.log 2>&1 & echo started pid \$!"
    printf "모델 로딩 대기"
    for i in $(seq 1 40); do sleep 6; if up; then printf "\n✓ 준비됨 (%ds)\n" $((i*6)); exit 0; fi; printf "."; done
    printf "\n⚠ 240s 내 응답 없음 — 원격 server.log 확인\n"; exit 1 ;;
  status)  if up; then echo "● 실행 중 ($URL)"; else echo "○ 죽음"; fi ;;
  stop)    ssh "$HOST" "pkill -f mlx_vlm.server" 2>/dev/null && echo "종료 신호 전송" || echo "프로세스 없음" ;;
  restart) "$0" stop; sleep 3; "$0" start ;;
  watch)
    echo "[gemma watchdog] 60s 간격 점검 시작 (Ctrl-C 종료)"
    while true; do
      if ! up; then echo "[$(date '+%F %T')] 서버 무응답 → 재시작"; "$0" start; fi
      sleep 60
    done ;;
  test)
    curl -s "$URL/chat/completions" -H 'Content-Type: application/json' \
      -d "{\"model\":\"$MODEL\",\"messages\":[{\"role\":\"user\",\"content\":\"1+1? 숫자만\"}],\"max_tokens\":10}" \
      | python3 -c "import sys,json;print('생성:',json.load(sys.stdin)['choices'][0]['message']['content'])" ;;
  *) echo "사용법: $0 {start|status|stop|restart|watch|test}"; exit 1 ;;
esac
