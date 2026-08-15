#!/usr/bin/env bash
# 바인드마운트에 쌓인 root 소유 파일을 호스트 사용자로 되돌린다.
#
# ★왜 필요한가: dev 컨테이너가 root 로 돈다. 레포는 `..:/app` 로 바인드마운트라, 컨테이너가 만든
#   파일은 호스트에서 root 소유로 남는다. 호스트 사용자는 그걸 못 고치고, 그래서 rsync/git 이
#   조용히 막힌다 — 실제로 그 상태가 **두 달간** 후처리 동기화를 세워놨고 아무도 몰랐다.
#   조용한 게 문제였다. 그래서 고치는 것보다 **소리를 내는 것**이 이 스크립트의 목적이다.
#
# ★왜 컨테이너로 chown 하나: 호스트 사용자는 root 소유 파일의 소유권을 못 바꾼다(sudo 없이).
#   컨테이너는 root 이고 같은 마운트를 보므로, 거기서 chown 하면 sudo 없이 해결된다.
#
# ★근본 해결은 따로다: `docker-compose.dev.yml` 에 `user: "1000:1000"`. 다만 named volume
#   (node_modules/.venv)의 소유권까지 같이 옮겨야 해서 정지 창이 필요하다. 그때까지 이걸로 버틴다.
#
# 사용: bash scripts/ops/heal_file_ownership.sh [--check]
#   --check  고치지 않고 개수만 보고한다(게이트용, 있으면 exit 1)
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CONTAINER="${MS_WEB_CONTAINER:-deploy-web-1}"
UID_="$(id -u)"; GID_="$(id -g)"
CHECK=0; [ "${1:-}" = "--check" ] && CHECK=1

cd "$REPO" || exit 2

# named volume 의 마운트포인트는 성질이 다르다 — 도커가 만든 **빈** 디렉터리이고 gitignore 대상이며,
# 컨테이너 안에서 chown 해도 호스트 엔트리는 안 바뀐다(볼륨이 그 자리를 가리므로). 고칠 수 없고
# 고칠 필요도 없다. 이걸 실패로 세면 게이트가 늑대소년이 되므로 따로 센다.
is_volume_mountpoint() {
  [ -d "$1" ] && [ -z "$(ls -A "$1" 2>/dev/null)" ] && git check-ignore -q "$1" 2>/dev/null
}

BAD=(); SKIP=()
while IFS= read -r p; do
  if is_volume_mountpoint "$p"; then SKIP+=("$p"); else BAD+=("$p"); fi
done < <(find . -not -user "$UID_" -not -path './.git/*' 2>/dev/null)
N=${#BAD[@]}

if [ ${#SKIP[@]} -gt 0 ]; then
  echo "ℹ️  볼륨 마운트포인트 ${#SKIP[@]}개는 건너뛴다(빈 디렉터리·gitignore·chown 불가): ${SKIP[*]}"
fi

if [ "$N" -eq 0 ]; then
  echo "✅ 소유권 — 남의 소유 파일 없음"
  exit 0
fi

echo "⚠️  소유권 — 호스트 사용자($UID_) 것이 아닌 파일 $N개"
printf '   %s\n' "${BAD[@]:0:8}"
[ "$N" -gt 8 ] && echo "   … 외 $((N - 8))개"

if [ "$CHECK" -eq 1 ]; then
  echo "   (--check 모드 — 고치지 않았다)"
  exit 1
fi

if ! docker ps --format '{{.Names}}' | grep -qx "$CONTAINER"; then
  echo "🔴 컨테이너 '$CONTAINER' 가 없다 — chown 할 수단이 없다."
  echo "   컨테이너를 띄우고 다시 돌리거나, MS_WEB_CONTAINER 로 이름을 지정한다."
  exit 1
fi

# 컨테이너 안 경로는 /app. 전체를 훑지 않고 문제가 된 것만 고친다(빠르고, 의도가 남는다).
printf '%s\n' "${BAD[@]}" | sed 's|^\./|/app/|' \
  | docker exec -i "$CONTAINER" xargs -r -d '\n' chown -h "$UID_:$GID_" 2>/dev/null

LEFT="$(find . -not -user "$UID_" -not -path './.git/*' 2>/dev/null | wc -l)"
if [ "$LEFT" -eq 0 ]; then
  echo "✅ $N개 되돌렸다 → $UID_:$GID_"
else
  echo "🔴 $((N - LEFT))개만 되돌렸다. $LEFT개 남음 — 수동 확인 필요."
  exit 1
fi
