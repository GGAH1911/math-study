#!/usr/bin/env bash
# ============================================================================
# math-study dev 서버 관리 — Claude Code 와 완전히 무관하게 동작.
#
#   ./server.sh start     서버 시작 (독립 세션 백그라운드 + 크래시 자동 재시작)
#   ./server.sh stop      서버 종료 (자식 node/vite/esbuild 까지 일괄)
#   ./server.sh restart   재시작
#   ./server.sh status    상태 + 접속 주소
#   ./server.sh logs      로그 실시간 (tail -f, Ctrl-C 로 빠져나옴)
#
# 핵심: setsid 로 "새 세션 리더"가 되어 띄운 셸(또는 Claude)이 죽어도 생존.
#       watchdog 루프가 astro 가 죽으면 3초 뒤 자동 재시작 → "안 꺼짐".
# ============================================================================
set -uo pipefail

# ─── 경로: 스크립트 위치 기준 자동 탐지 (worktree 가 옮겨가도 동작) ───────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SELF="$SCRIPT_DIR/$(basename "${BASH_SOURCE[0]}")"
WEB_DIR="${MATH_STUDY_WEB:-$SCRIPT_DIR/web}"

HOST="0.0.0.0"                              # Tailscale/LAN 접속용 전체 바인드
PORT="${MATH_STUDY_PORT:-4323}"
PID_FILE="${MATH_STUDY_PID:-/tmp/math-study-server.pid}"
LOG_FILE="${MATH_STUDY_LOG:-/tmp/math-study-server.log}"
TS_HOST="${MATH_STUDY_TSHOST:-tme-laptop.tailf47aa4.ts.net}"  # 풀 MagicDNS 이름 (짧은 .ts.net 은 resolve 안 됨)

g=$'\e[32m'; r=$'\e[31m'; y=$'\e[33m'; d=$'\e[2m'; x=$'\e[0m'

server_pid() { [[ -f "$PID_FILE" ]] && cat "$PID_FILE" 2>/dev/null; }
is_running() { local p; p="$(server_pid)"; [[ -n "${p:-}" ]] && kill -0 "$p" 2>/dev/null; }
port_busy()  { ss -tlnp 2>/dev/null | grep -q ":${PORT} "; }

urls() {
  local tip; tip="$(tailscale ip -4 2>/dev/null | head -1)"
  echo "  ${d}로컬      ${x}http://localhost:${PORT}"
  echo "  ${d}Tailscale ${x}http://${TS_HOST}:${PORT}"
  [[ -n "$tip" ]] && echo "  ${d}    또는  ${x}http://${tip}:${PORT}  ${d}(IP — 항상 확실)${x}"
}

start() {
  if is_running; then
    echo "${g}이미 실행 중${x} (PID $(server_pid))"; urls; return 0
  fi
  if port_busy; then
    echo "${y}⚠ 포트 ${PORT} 가 이미 사용 중인데 우리 PID 기록이 없음.${x} 확인:"
    ss -tlnp 2>/dev/null | grep ":${PORT} "
    echo "  → 그 프로세스를 끄거나 './server.sh stop' 후 다시 시도."
    return 1
  fi
  if [[ ! -x "$WEB_DIR/node_modules/.bin/astro" ]]; then
    echo "${r}✗ astro 없음:${x} $WEB_DIR/node_modules"
    echo "  먼저: (cd '$WEB_DIR' && npm install)"; return 1
  fi
  echo "서버 시작 중... ${d}($WEB_DIR)${x}"
  # setsid: 독립 세션 리더 → 부모가 죽어도 생존.
  # 내부 bash 가 자기 PID(=세션·그룹 리더, exec 후에도 불변) 를 기록 후 watchdog 실행.
  setsid bash -c "echo \$\$ > '$PID_FILE'; exec '$SELF' __watchdog" \
    </dev/null >"$LOG_FILE" 2>&1 &
  disown 2>/dev/null || true
  printf "  ${d}content sync 대기${x}"
  local i
  for i in $(seq 1 90); do
    if port_busy; then
      printf "\n${g}✓ 실행 중${x} (PID $(server_pid))\n"; urls
      echo "  ${d}로그: ./server.sh logs${x}"; return 0
    fi
    is_running || { printf "\n${r}✗ watchdog 가 떠 있지 않음.${x} 로그:\n"; tail -n 15 "$LOG_FILE"; return 1; }
    sleep 2; printf "."
  done
  printf "\n${y}⚠ 180초 내 포트 안 열림 (sync 가 더 걸리거나 에러).${x} 로그 끝:\n"
  tail -n 15 "$LOG_FILE"; return 1
}

stop() {
  local p; p="$(server_pid)"
  if [[ -z "${p:-}" ]]; then echo "꺼져 있음 ${d}(PID 파일 없음)${x}"; return 0; fi
  if ! kill -0 "$p" 2>/dev/null; then echo "꺼져 있음 ${d}(잔존 PID 정리)${x}"; rm -f "$PID_FILE"; return 0; fi
  echo "종료 중 (PID $p, 프로세스 그룹 일괄)..."
  kill -TERM -"$p" 2>/dev/null || kill -TERM "$p" 2>/dev/null
  local i
  for i in $(seq 1 12); do kill -0 "$p" 2>/dev/null || break; sleep 0.5; done
  if kill -0 "$p" 2>/dev/null; then kill -KILL -"$p" 2>/dev/null || kill -KILL "$p" 2>/dev/null; fi
  rm -f "$PID_FILE"
  echo "${g}✓ 종료됨${x}"
}

status() {
  if is_running; then
    echo "${g}● 실행 중${x} (PID $(server_pid))"; urls
    echo "  ${d}로그: $LOG_FILE${x}"
  else
    echo "${r}○ 꺼져 있음${x}"
    port_busy && echo "  ${y}(단, 포트 ${PORT} 는 다른 프로세스가 점유 중)${x}"
  fi
  return 0
}

# ─── 내부 전용: 독립 세션 안에서 도는 watchdog 루프 (직접 호출 X) ─────────────
watchdog() {
  trap 'exit 0' TERM INT          # stop 의 그룹-TERM 시 재시작 없이 깔끔히 종료
  cd "$WEB_DIR" || exit 1
  while true; do
    echo "[$(date '+%F %T')] astro dev 시작 (host=$HOST port=$PORT)"
    node_modules/.bin/astro dev --host "$HOST" --port "$PORT" &
    local astro_pid=$!
    # 헬스 모니터: astro 가 *살아는 있는데 HTTP 무응답*(=행, Vite program-reload
    # 행 등)이면 kill-0 으론 못 잡는다 → 실제 응답을 N연속 못 받으면 astro 를
    # 강제종료해 아래 while 루프가 재시작하게 만든다. (크래시는 기존대로 자동복구.)
    ( sleep 90                                          # 콜드 기동(content sync) 유예
      fails=0
      while kill -0 "$astro_pid" 2>/dev/null; do
        if curl -s -o /dev/null --max-time 10 "http://127.0.0.1:${PORT}/" 2>/dev/null; then
          fails=0
        else
          fails=$((fails + 1))
          if [ "$fails" -ge 3 ]; then                   # ≈36초 연속 무응답 = 행
            echo "[$(date '+%F %T')] ⚠ HTTP ${fails}연속 무응답 — astro(행) 강제종료 → 재시작 유도"
            kill -KILL "$astro_pid" 2>/dev/null
            break
          fi
        fi
        sleep 12
      done ) &
    local mon_pid=$!
    # ── HMR watcher 갱신 모니터 (4323 전용; STABLE=4324 는 수동 재시작 설계라 제외) ──
    # corrector/ingest/box_backfill 등 대량 배치가 docs md 를 다발로 다시 쓰면 inotify
    # 이벤트 큐(max_queued_events)를 넘쳐 chokidar watcher 가 조용히 desync → 이후 단일
    # 편집이 HMR 에 안 잡힌다(서버 재시작 전까지). 배치를 감지해 *가라앉은 뒤* astro 를
    # 한 번 kill → 위 while 루프가 fresh watcher 로 재기동시킨다. 평소 단일 편집은 영향 X.
    local hmr_pid=""
    if [ -z "${STABLE:-}" ]; then
      ( sleep 90                                          # 콜드 기동(content sync) 유예
        mark="${LOG_FILE%.log}.hmrmark"; touch "$mark"
        batch=0
        while kill -0 "$astro_pid" 2>/dev/null; do
          sleep 25
          changed=$(find "$SCRIPT_DIR/docs" -name '*.md' -newer "$mark" 2>/dev/null | wc -l)
          touch "$mark"
          if [ "$changed" -ge 25 ]; then                  # 25s 창에 md 25개+ = 배치(수동편집 아님)
            [ "$batch" -eq 0 ] && echo "[$(date '+%F %T')] 📦 배치 감지(${changed} md 변경) — 가라앉으면 4323 HMR 갱신"
            batch=1
          elif [ "$batch" -eq 1 ] && [ "$changed" -le 3 ]; then   # 배치 후 잠잠 = 종료
            echo "[$(date '+%F %T')] 📦 배치 종료 — 4323 재시작(HMR watcher 갱신)"
            kill -KILL "$astro_pid" 2>/dev/null; break
          fi
        done ) &
      hmr_pid=$!
    fi
    wait "$astro_pid" 2>/dev/null
    local code=$?
    kill "$mon_pid" 2>/dev/null    # 헬스 모니터 정리
    [ -n "$hmr_pid" ] && kill "$hmr_pid" 2>/dev/null    # HMR 모니터 정리
    echo "[$(date '+%F %T')] astro 종료(exit $code) — 3초 뒤 재시작"
    sleep 3
  done
}

case "${1:-}" in
  start)      start ;;
  stop)       stop ;;
  restart)    stop; sleep 1; start ;;
  status)     status ;;
  logs)       tail -n 40 -f "$LOG_FILE" ;;
  __watchdog) watchdog ;;          # 내부 전용
  *) echo "사용법: $0 {start|stop|restart|status|logs}"; exit 1 ;;
esac
