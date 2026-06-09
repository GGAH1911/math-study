#!/bin/sh
# 모든 마이그레이션을 순서대로 적용. 멱등(각 .sql 이 IF NOT EXISTS/guard 사용).
#   사용: ./db/migrate.sh   (env MATH_STUDY_DATABASE_URL 로 대상 override)
set -e
DB="${MATH_STUDY_DATABASE_URL:-postgresql://mathstudy:mathstudy@127.0.0.1:5434/mathstudy}"
DIR="$(cd "$(dirname "$0")/migrations" && pwd)"
for f in "$DIR"/*.sql; do
  printf 'applying %s ... ' "$(basename "$f")"
  psql "$DB" -v ON_ERROR_STOP=1 -q -f "$f" >/dev/null
  echo ok
done
echo "✓ 모든 마이그레이션 적용됨"
