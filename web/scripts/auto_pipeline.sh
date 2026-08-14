#!/bin/bash
# 자율 파이프라인 (사용자 취침 중 무인 실행, setsid로 Claude와 분리).
#   1) extract 배치 완료 대기 → extract+코드 커밋·푸시
#   2) corrector_batch 반복: 검증게이트·Sonnet자가치유·빌드체크 내장. 쿼터 소진 시 5h 대기 후 재개.
#   3) 회차마다 corrected 커밋·푸시. 빌드체크 실패 시 즉시 중단(서버 보호).
set -u
# ⚠️ **2026-06 세션 전용 일회성 유물이다.** 아래 커밋 메시지에 그때의 세션 URL 과 작업 내용이
#    그대로 박혀 있어, 지금 돌리면 무관한 변경에 그 메시지가 붙는다.
#    ★예전엔 옛 머신 경로(`/home/insung/Projects/math-study`)를 cd 했다. 이전 후에도 그
#      **껍데기 디렉터리가 남아 cd 가 성공**하고, 이후 git("not a git repository")·node 가
#      전부 실패하는데 `set -e` 가 없어 **아무 일도 안 하며 무한 루프**를 돌았다(2026-08-15 감사).
#    되살리려면 커밋 메시지부터 새로 쓰고 AUTO_PIPELINE_OK=1 을 준다.
[ "${AUTO_PIPELINE_OK:-}" = "1" ] || {
  echo "⛔ auto_pipeline.sh 는 2026-06 세션 전용 일회성 스크립트다."
  echo "   커밋 메시지·config 를 지금 작업에 맞게 고친 뒤 AUTO_PIPELINE_OK=1 로 실행하라."
  exit 2
}
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)" || exit 1
LOG=/tmp/ingest_logs/auto_pipeline.log
mkdir -p /tmp/ingest_logs
exec >> "$LOG" 2>&1
SESS="Claude-Session: https://claude.ai/code/session_01VeuffwD9BWh7nnVVbh8LmW"
COAUTH="Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
echo "===== [$(date)] auto_pipeline 시작 ====="

# 1) extract 배치 완료 대기 (python -u -c 배치가 끝날 때까지)
while ps aux | grep -q '[p]ython3 -u -c'; do sleep 60; done
echo "[$(date)] extract 배치 완료"

# 1b) extract + 코드 커밋·푸시 (결정론, 안전)
git add -A docs/problems web/scripts web/src
if ! git diff --cached --quiet; then
  git commit -m "feat(corrector): extract 재적용(figures·표 복원, 표오인 reject) + 교정기 안전장치

- extract_figures: 좌우나란히 anchor, 표 단일셀(1×1) reject(조건박스 표오인 방지)
- corrector.mjs: 구분자 raw 출력(JSON.parse LaTeX 손상 폐지) + 검증게이트(제어문자·placeholder·중괄호·길이·선택지·\$) + Sonnet 자가치유 + 격리
- corrector_batch: 동시워커 + 100개마다 YAML 빌드체크(서버다운 차단)
- reconstruct: 방향A(\$ 제거) + (가)~(하) 빈칸박스 + (가)(나)(다) 줄분리/질문분리 + KaTeX nowrap

$COAUTH
$SESS"
  git push && echo "[$(date)] extract+코드 커밋·푸시 완료"
fi

# 2) corrector 반복 (쿼터 대기 재개)
ROUND=0
while true; do
  ROUND=$((ROUND+1))
  echo "[$(date)] === corrector 회차 $ROUND 시작 ==="
  # 동시성은 토큰과 무관(실측: cache_creation이 프롬프트별이라 매 콜 발생, 동시성 영향 0).
  #   속도만 좌우 → 10. (이전 "동시2=캐시적중으로 토큰 1/10" 주석은 헛다리라 제거.)
  # 로그는 회차별 파일로 보존 — corrector_run.log를 `>`로 덮어써 이전 회차 디버그 자료가
  #   날아가던 결함 수정(사라지면 로그가 아니다).
  RUNLOG=/tmp/ingest_logs/corrector_run_$ROUND.log
  CORR_CONC=10 node web/scripts/corrector_batch.mjs > "$RUNLOG" 2>&1
  tail -3 "$RUNLOG"
  REMAIN=$(grep -oP '남은대상 \K\d+' "$RUNLOG" | tail -1)

  # 회차 corrected 커밋·푸시
  git add -A docs/problems
  if ! git diff --cached --quiet; then
    git commit -m "chore(corrector): Gemini/Sonnet 교정 회차 $ROUND (남은 ${REMAIN:-?})

$COAUTH
$SESS"
    git push && echo "[$(date)] 회차 $ROUND 커밋·푸시"
  fi

  # 안전: 빌드체크 실패 → 즉시 중단
  if grep -q '빌드체크 실패' "$RUNLOG"; then
    echo "[$(date)] ⛔ 빌드체크 실패 — 파이프라인 중단(서버 보호)"; break
  fi
  # 완료
  if [ "${REMAIN:-1}" = "0" ]; then echo "[$(date)] ✅ 전부 교정 완료"; break; fi
  # 쿼터 소진 추정 → 10분마다 agy 헬스체크 → 응답 있으면 즉시 재개 (무작정 5h 대기 X)
  echo "[$(date)] 쿼터 소진 추정(남은 ${REMAIN:-?}) — 10분마다 헬스체크"
  while true; do
    sleep 600
    if timeout 60 claude -p "2+3 숫자만 답해." --model haiku --output-format json 2>/dev/null | grep -q '[0-9]'; then
      echo "[$(date)] agy 응답 확인 — 재개"; break
    fi
    echo "[$(date)] agy 아직 빈출력 — 10분 더 대기"
  done
done
echo "===== [$(date)] auto_pipeline 종료 ====="
