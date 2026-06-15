"""2019 고3 4월모의고사 나형 22번 — 파라미터 솔버 (수동 작성).
문제: 공비가 5인 등비수열 {a_n} 에 대하여 a_5/a_3 의 값. (a₁≠0) (답 25)
구조: a_5/a_3 = (a₁r⁴)/(a₁r²) = r² = 5² = 25.
재생산: (공비 r, 인덱스차) 파라미터화.
"""
import sympy as sp


def solve(r, i, j):
    a1 = sp.symbols('a1', nonzero=True)
    return sp.simplify((a1 * r ** (i - 1)) / (a1 * r ** (j - 1)))   # a_i/a_j = r^(i-j)


CANDIDATE = 25
assert solve(5, 5, 3) == CANDIDATE, solve(5, 5, 3)
print('VERIFY_PASS')
