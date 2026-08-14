#!/usr/bin/env python3
"""튜터와 **똑같은 sympy 환경**에서 코드를 실행한다.

★왜 따로 만드나: 헬퍼(assert_distance3d·assert_on_plane…)는 브라우저 워커의 헤더에만
  통째로 들어 있고, 로컬에는 sympy 자체가 없다. 검증하는 사람이 헤더를 손으로 흉내내면
  "튜터 환경에서는 되는데/안 되는데" 를 영영 못 맞춘다. 그래서 **워커 헤더를 그대로 뽑아**
  컨테이너 파이썬에 붙여 돌린다.

사용:  echo '<파이썬 코드>' | python3 scripts/ops/sympy_run.py
       python3 scripts/ops/sympy_run.py <파일>
"""
from __future__ import annotations
import re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKER = ROOT / 'web/public/pyodide-worker.js'
COMPOSE = ['docker', 'compose', '-f', str(ROOT / 'deploy/docker-compose.yml')]


def header() -> str:
    s = WORKER.read_text(encoding='utf-8')
    m = re.search(r'runPythonAsync\(`(.*?)\n`\)', s, re.S)
    if not m:
        sys.exit('워커에서 헤더를 못 찾았다 — pyodide-worker.js 구조가 바뀌었나?')
    return m.group(1).replace('\\`', '`').replace('\\$', '$')


def main() -> int:
    code = Path(sys.argv[1]).read_text(encoding='utf-8') if len(sys.argv) > 1 else sys.stdin.read()
    r = subprocess.run(COMPOSE + ['exec', '-T', 'web', '/app/.venv/bin/python', '-'],
                       input=(header() + '\n' + code).encode('utf-8'),
                       capture_output=True, timeout=300)
    sys.stdout.write(r.stdout.decode('utf-8', 'replace'))
    err = r.stderr.decode('utf-8', 'replace')
    if err.strip():
        sys.stderr.write(err)
    return r.returncode


if __name__ == '__main__':
    sys.exit(main())
