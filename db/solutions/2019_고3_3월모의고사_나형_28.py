"""2019 고3 3월모의고사 나형 28번 — 파라미터화 솔버.

문제 구조:
  U = {1, 2, ..., limit} 중 exclude_divisor 의 배수가 아닌 자연수들의 집합.
  A ⊂ U, n(A) = n, A의 모든 원소의 합 = target.
  A의 원소를 오름차순 x_1 < x_2 < ... < x_n 으로 나열했을 때,
  교대합 x_n - x_{n-1} + x_{n-2} - ... ± x_1 의 최댓값을 구한다.

원문제: limit=30, exclude_divisor=3, n=4, target=100  →  x_4-x_3+x_2-x_1 의 최댓값 = 10.

파라미터화 포인트:
  - limit           : 전체집합 U의 상한 (원문제 30)
  - exclude_divisor : U에서 제외하는 배수의 기준 (원문제 3의 배수 제외)
  - n               : 부분집합 A의 원소 개수 (원문제 4)
  - target          : A의 원소합 조건 (원문제 100)
  limit 과 target 을 바꾸면 탐색 대상 조합 자체가 달라져 최댓값이 실제로 바뀐다.
  exclude_divisor 를 바꾸면 U의 구성 원소가 달라져 역시 최댓값이 바뀐다.
"""
from itertools import combinations

import sympy as sp


def build_universe(limit, exclude_divisor):
    """U = {1..limit} 중 exclude_divisor의 배수가 아닌 자연수 (sympy Mod로 판정)."""
    return [v for v in range(1, limit + 1) if sp.Mod(v, exclude_divisor) != 0]


def alt_sum(xs_sorted):
    """오름차순 원소열에 대해 x_n - x_{n-1} + x_{n-2} - ... ± x_1 계산 (sympy로 합산)."""
    n = len(xs_sorted)
    # i번째(1-indexed, 오름차순) 원소의 부호는 (-1)**i : x_1은 -, x_2는 +, x_3은 -, x_4는 + ...
    terms = [((-1) ** i) * sp.Integer(x) for i, x in enumerate(xs_sorted, start=1)]
    return int(sp.Add(*terms))


def solve(prm):
    limit = prm['limit']
    exclude_divisor = prm['exclude_divisor']
    n = prm['n']
    target = prm['target']

    U = build_universe(limit, exclude_divisor)
    if len(U) < n:
        raise ValueError("조건을 만족하는 원소 개수가 부족합니다.")

    best = None
    for combo in combinations(U, n):
        # 원소합 조건을 sympy Eq로 실제 판정
        if sp.Eq(sp.Add(*[sp.Integer(c) for c in combo]), sp.Integer(target)) == True:
            xs = sorted(combo)
            val = alt_sum(xs)
            best = val if best is None else max(best, val)

    if best is None:
        raise ValueError(f"합이 {target}인 {n}원소 부분집합이 U 안에 존재하지 않습니다.")
    return best


def statement(prm):
    limit = prm['limit']
    exclude_divisor = prm['exclude_divisor']
    n = prm['n']
    target = prm['target']

    # 교대합 수식 문자열 생성: x_n - x_{n-1} + x_{n-2} - ... ± x_1
    parts = [f"x_{n}"]
    for j in range(1, n):
        sign = '-' if j % 2 == 1 else '+'
        parts.append(f"{sign}x_{n - j}")
    expr = ''.join(parts)

    idx_list = ', '.join(f"x_{i}" for i in range(1, n + 1))

    return (
        f"전체집합 U = \\{{ x | x \\text{{는 }} {exclude_divisor} \\text{{의 배수가 아닌 }} "
        f"{limit} \\text{{ 이하의 자연수}} \\}} 의 부분집합 A에 대하여 n(A)={n}이고 "
        f"집합 A의 모든 원소의 합은 {target}이다. 집합 A의 모든 원소를 작은 수부터 크기순으로 "
        f"나열한 것을 {idx_list}라 할 때, {expr}의 최댓값을 구하시오."
    )


CANDIDATE = 10  # ★원문제 정답, 절대 바꾸지 않음
PARAMS = dict(limit=30, exclude_divisor=3, n=4, target=100)

print(statement(PARAMS))
print('VERIFY_PASS' if solve(PARAMS) == CANDIDATE else 'VERIFY_FAIL')
