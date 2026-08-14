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


#: 답을 실제로 바꿔야 하는 파라미터의 최소 개수. 1개면 손잡이가 하나뿐이라
#: "같은 문제의 배수" 정도밖에 못 만든다 — 유사문제 재생성이라 부르기 어렵다.
MIN_LIVE = 2


def _perturbations(v, sp):
    """파라미터 하나를 흔드는 여러 방법. **한 방법이라도 답을 바꾸면 살아있다.**

    ★+1 하나만 시도하면 멀쩡한 파라미터를 죽었다고 오판한다: 불리언은 +1 이 무의미하고,
      보기 목록(list)은 원소를 건드려야 하며, +1 이 우연히 같은 답을 주는 경우도 있다.
    """
    if isinstance(v, bool):
        return [not v]
    if isinstance(v, (int, float)) or getattr(v, 'is_number', False):
        out = [v + 1, v + 2]
        if v != 0:
            out.append(v * 2)
        return out
    if isinstance(v, (list, tuple)):
        out = []
        for i, x in enumerate(v):                      # 보기 목록은 원소별로 흔든다
            try:
                nx = sp.nsimplify(x) + 1
            except Exception:
                continue
            nv = list(v)
            nv[i] = nx
            out.append(type(v)(nv) if isinstance(v, tuple) else nv)
        return out
    return []


def _check_variants(m, variants, base, sp) -> list[str]:
    """`VARIANTS` 로 제시된 파라미터 조합들이 **실제로 새 문제를 만들어내는지** 본다.

    각 항목은 PARAMS 에 덮어쓸 부분 dict. 전부 예외 없이 풀려야 하고, 그중 최소
    MIN_LIVE 개가 **원문제와 다른 답**을 내야 한다(그래야 재생성이라 부를 수 있다).
    """
    bad: list[str] = []
    if len(variants) < MIN_LIVE:
        return [f'VARIANTS 가 {len(variants)}개뿐 (최소 {MIN_LIVE})']
    answers = []
    for i, ov in enumerate(variants, 1):
        if not isinstance(ov, dict) or not ov:
            bad.append(f'VARIANTS[{i}] 가 dict 가 아니다')
            continue
        try:
            got = sp.nsimplify(m.solve({**m.PARAMS, **ov}))
        except Exception as e:
            bad.append(f'VARIANTS[{i}] {ov} → 예외: {type(e).__name__}: {e}')
            continue
        if not getattr(got, 'is_number', False) or got.has(sp.zoo, sp.nan, sp.oo):
            bad.append(f'VARIANTS[{i}] {ov} → 유효한 수가 아니다: {got}')
            continue
        answers.append(got)
    moved = [a for a in answers if sp.simplify(a - base) != 0]
    if len(moved) < MIN_LIVE:
        bad.append(f'원문제와 답이 다른 VARIANTS 가 {len(moved)}개뿐 (최소 {MIN_LIVE})')
    return bad


def load(path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)          # ★import 시 VERIFY_PASS 를 찍는 구조라 출력이 섞인다
    return mod


def check(stem: str) -> list[str]:
    return check_path(SOL / f'{stem}.py')


def check_path(path: pathlib.Path) -> list[str]:
    """솔버 **파일 하나**를 검사한다.

    ★`--file` 로 노출해 둔 이유: 파라미터화 배치의 에이전트가 **이 게이트를 직접 돌려
      통과할 때까지 고칠 수 있어야** 한다. 손으로 짐작하게 두면 절반이 떨어진다
      (2026-08-14 실측: 게이트 없이 48% 통과). 이 파일은 sympy 말고는 의존이 없어
      스크래치 폴더에 그대로 복사해 쓸 수 있다 — 사본이 아니라 **원본을 복사**하므로
      규격이 갈라지지 않는다.
    """
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
    #
    # ★2026-08-14 강화: 예전엔 "하나라도 움직이면 통과" 였다. 그런데 그 잣대로는
    #   **선언만 해 두고 실제로는 안 쓰는 파라미터**가 얼마든지 통과한다(실측: 46건 중
    #   8개 선언에 1개만 살아 있던 솔버가 있었다). 유사문제를 뽑으려면 돌릴 손잡이가
    #   여럿이어야 하므로 **살아 있는 파라미터 2개 이상**을 요구한다.
    #   1개짜리는 사실상 "그 문제 하나 + 스칼라 배" 밖에 못 만든다.
    #
    # ★결합 파라미터 예외(2026-08-14): "자연수 m,n 을 구하라" 류는 파라미터가 서로 묶여
    #   있어서 **하나만 흔들면 정수해가 깨진다**(공통_22: sx 를 1→2 로만 바꾸면 해 없음,
    #   sx·sy 를 함께 2배 하면 성립). 그런 솔버는 `VARIANTS` 로 **성립하는 조합**을 직접
    #   제시하면 된다 — 유사문제 재생성 능력을 더 직접적으로 증명하는 방식이다.
    variants = getattr(m, 'VARIANTS', None)
    if variants:
        return bad + _check_variants(m, variants, base, sp)
    dead, live = [], []
    for k, v in m.PARAMS.items():
        for nv in _perturbations(v, sp):
            try:
                got = sp.nsimplify(m.solve({**m.PARAMS, k: nv}))
            except Exception:
                continue
            if not getattr(got, 'is_number', False) or got.has(sp.zoo, sp.nan, sp.oo):
                continue
            if sp.simplify(got - base) != 0:
                live.append(k)
                break
        else:
            dead.append(k)
    if not live:
        bad.append('어떤 파라미터를 바꿔도 답이 그대로 — PARAMS 가 장식이다')
    elif len(live) < MIN_LIVE:
        bad.append(f'답을 바꾸는 파라미터가 {len(live)}개뿐 (최소 {MIN_LIVE}) — '
                   f'살아있음 {live} · 장식 {dead}')
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('stems', nargs='*')
    ap.add_argument('--round', default='')
    ap.add_argument('--file', default='', help='솔버 .py 경로 하나만 검사(레포 밖에서도 동작)')
    a = ap.parse_args()
    if a.file:
        bad = check_path(pathlib.Path(a.file))
        if bad:
            print(f'🔴 {a.file}')
            for b in bad:
                print(f'     {b}')
            print('\n미충족 — 위 항목을 고치고 다시 실행하세요.')
            return 1
        print('✅ 파라미터화 규격 충족')
        return 0
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
