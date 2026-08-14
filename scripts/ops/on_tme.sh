#!/usr/bin/env bash
# ============================================================================
# math-study 명령 라우터 — "어느 기계에서 실행하든 같은 문자열"
#
#   scripts/ops/on_tme.sh 'docker compose -f deploy/docker-compose.yml ps'
#
# tme 에서 실행하면  → 레포로 cd 한 뒤 그대로 로컬 실행
# 그 밖(맥북 등)이면 → ssh -o BatchMode=yes tme 로 같은 명령을 넘겨 실행
#
# 왜: 서비스·DB·크론이 전부 tme 에만 있다. 헬스체크와 셧다운 게이트를 기계마다
#     다르게 적으면 두 벌이 갈라진다. .session-protocol.yml 과 CLAUDE.md 는 이
#     라우터 하나만 부르고, 어디서 세션을 열든 같은 절차가 돈다.
#     (맥북 원격개발 세션 ↔ tme 직결 세션 동일 프로토콜)
#
# 환경변수:
#   MATH_STUDY_TME_REPO  tme 쪽 레포 경로 (기본 /home/insung/math-study)
#   MATH_STUDY_TME_HOST  ssh 대상 (기본 tme — ~/.ssh/config 의 Host 이름)
# ============================================================================
set -uo pipefail

REPO_TME="${MATH_STUDY_TME_REPO:-/home/insung/math-study}"
SSH_HOST="${MATH_STUDY_TME_HOST:-tme}"

if [ "$#" -eq 0 ]; then
  echo "사용법: $0 '<tme 에서 돌릴 명령>'" >&2
  exit 2
fi

# tme 판정: 호스트명(대소문자 무시). 컨테이너/워크트리에서도 동작하도록 레포 존재도 함께 본다.
host_short="$(hostname -s 2>/dev/null || hostname 2>/dev/null)"
host_lc="$(printf '%s' "${host_short:-}" | tr '[:upper:]' '[:lower:]')"

if [ "$host_lc" = "tme" ] && [ -d "$REPO_TME" ]; then
  cd "$REPO_TME" || exit 1
  exec bash -c "$*"
fi

# ★원격 페이로드는 반드시 `bash -c '<...>'` 한 겹으로 감싼다. 두 가지 이유:
#   ① tme 로그인 셸은 zsh 다 — 명령 문자열을 bash 문법으로 쓰고 싶다.
#   ② `cd X && cmd` 를 날것으로 넘기면 중간의 명령 재작성 계층(rtk 래퍼 등)이 선행
#      `cd X &&` 를 삼켜 cwd 가 홈으로 떨어진다(2026-08-14 실측: 게이트가 전부
#      "can't open file '/home/insung/scripts/...'" 로 죽었다). 한 겹 감싸면 안 건드린다.
payload="cd '$REPO_TME' && $*"
exec ssh -o BatchMode=yes "$SSH_HOST" "bash -c $(printf '%q' "$payload")"
