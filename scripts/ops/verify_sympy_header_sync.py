#!/usr/bin/env python3
"""sympy 헤더가 **서버와 브라우저에서 같은가**를 검사한다.

★왜: 헤더가 두 곳에 복사돼 있다 —
   서버 `web/src/pages/api/sympy.ts` / 브라우저 `web/public/pyodide-worker.js`.
   튜터는 **브라우저 Pyodide 를 1차**로 쓰고 서버는 폴백이다. 그래서 서버만 고치면
   사용자에게는 아무 변화가 없다. 2026-08-14 에 실제로 그렇게 됐다 — 3D 작도 헬퍼를
   서버에만 넣고 "고쳤다" 고 보고했는데 브라우저에는 없어 여전히 막혀 있었다.

여기서는 **함수 이름 집합**만 본다. 본문까지 비교하면 사소한 주석 차이로 빨개지고,
빨간 게이트는 곧 아무도 안 보는 게이트가 된다.
"""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRV = ROOT / 'web/src/pages/api/sympy.ts'
BRW = ROOT / 'web/public/pyodide-worker.js'
DEF = re.compile(r'^def ([A-Za-z_][A-Za-z_0-9]*)\(', re.M)


def defs(p: Path) -> set[str]:
    return set(DEF.findall(p.read_text(encoding='utf-8')))


def main() -> int:
    s, b = defs(SRV), defs(BRW)
    only_s, only_b = sorted(s - b), sorted(b - s)
    if not only_s and not only_b:
        print(f'✅ sympy 헤더 동기 — 함수 {len(s)}개 일치')
        return 0
    print('🔴 sympy 헤더가 어긋났다 — 브라우저가 1차이므로 사용자에게 보이는 건 브라우저 쪽이다')
    for n in only_s: print(f'   서버에만 있음: {n}  → pyodide-worker.js 에도 넣어라')
    for n in only_b: print(f'   브라우저에만 있음: {n}  → api/sympy.ts 에도 넣어라')
    return 1


if __name__ == '__main__':
    sys.exit(main())
