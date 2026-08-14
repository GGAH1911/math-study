#!/usr/bin/env python3
"""솔버가 **파라미터화** 규격을 지키는지 검사한다.

★왜: scripts/CLAUDE.md 는 솔버의 **핵심 용도를 "유사문제 무한 재생성"** 이라고 못 박는다.
  그런데 hardcode_gate 는 ①실제 수식 풀이 ②원본 통과 ③변이 실패만 본다 — **파라미터화는
  아예 안 본다.** 그래서 숫자가 박힌 '검증기' 가 통과해 왔다(2026-08-14 실측: 솔버 4,192개 중
  PARAMS 를 가진 것 2개). 이름만 "솔버" 로 바꾸고 게이트는 옛 정의 그대로였던 것이다.

요구 규격:
  PARAMS = dict(...)            문제를 정하는 값들
  def solve(prm) -> 답          조건 → 답 (문제의 수학 구조)
  CANDIDATE = <정답>            solve(PARAMS) 가 이 값을 재현해야 한다

검사 4가지:
  ① PARAMS · solve 존재  ② solve(PARAMS) == CANDIDATE (원문제 재현)
  ③ 파라미터를 바꾸면 답도 **실제로 바뀐다**(장식용 PARAMS 차단)
  ④ 바꾼 답이 유효한 수(허수·NaN·예외 아님)

사용: python3 scripts/ops/verify_solver_params.py <slug ...> | --round <라운드>
"""
from __future__ import annotations
import argparse, importlib.util, pathlib, sys, traceback

ROOT = pathlib.Path(__file__).resolve().parents[2]
SOL = ROOT / 'db' / 'solutions'


def load(path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)          # ★import 시 VERIFY_PASS 를 찍는 구조라 출력이 섞인다
    return mod


def check(stem: str) -> list[str]:
    path = SOL / f'{stem}.py'
    if not path.exists():
        return ['솔버 파일 없음']
    bad: list[str] = []
    try:
        m = load(path)
    except Exception as e:
        return [f'import 실패: {e}']
    if not isinstance(getattr(m, 'PARAMS', None), dict) or not m.PARAMS:
        bad.append('PARAMS dict 없음 — 파라미터화 안 됨(검증기에 머물러 있다)')
    if not callable(getattr(m, 'solve', None)):
        bad.append('solve(prm) 없음')
    if bad:
        return bad
    import sympy as sp
    try:
        base = sp.nsimplify(m.solve(m.PARAMS))
    except Exception as e:
        return [f'solve(PARAMS) 예외: {e}']
    if sp.simplify(base - sp.nsimplify(m.CANDIDATE)) != 0:
        bad.append(f'원문제 재현 실패: solve(PARAMS)={base}, CANDIDATE={m.CANDIDATE}')
    # ③ 파라미터를 흔들어 답이 따라 바뀌는지
    moved = 0
    for k, v in m.PARAMS.items():
        try:
            nv = v + 1 if isinstance(v, (int, float)) or getattr(v, 'is_number', False) else None
            if nv is None:
                continue
            got = sp.nsimplify(m.solve({**m.PARAMS, k: nv}))
            if not got.is_number or got.has(sp.zoo, sp.nan, sp.oo):
                continue
            if sp.simplify(got - base) != 0:
                moved += 1
        except Exception:
            continue
    if moved == 0:
        bad.append('어떤 파라미터를 바꿔도 답이 그대로 — PARAMS 가 장식이다')
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('stems', nargs='*')
    ap.add_argument('--round', default='')
    a = ap.parse_args()
    stems = a.stems
    if a.round:
        stems = sorted(p.stem for p in (ROOT / 'docs' / 'problems').rglob('*.md') if a.round in str(p))
    fails = 0
    for s in stems:
        bad = check(s)
        if bad:
            fails += 1
            print(f'🔴 {s}')
            for b in bad:
                print(f'     {b}')
    print(f'\n{len(stems)}건 중 {fails}건 미충족' if fails else f'\n✅ {len(stems)}건 전부 파라미터화 규격 충족')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
