#!/bin/bash
# 모델 가용성 프로브 크론 래퍼.
#   크론에서 복잡한 인용부호·키 추출을 직접 하면 깨지기 쉬워 래퍼로 뺐다(다른 ops 크론과 같은 방식).
#   컨테이너에서 실행하는 이유: 호스트엔 node 의존성이 없고, 컨테이너엔 다 있다([[project_tme_deploy]]).
set -uo pipefail
REPO=/home/insung/math-study
KEY=$(grep -oP '^NOUS_API_KEY=\K.*' /home/insung/.hermes/.env 2>/dev/null | tr -d "\"'" | head -1)
[ -z "$KEY" ] && { echo "$(date -Is) NOUS_API_KEY 없음" >&2; exit 1; }
cd "$REPO/deploy" || exit 1
docker compose exec -T -e NOUS_API_KEY="$KEY" -e WT_REPO=/app web \
  node /app/web/scripts/model_probe.mjs
