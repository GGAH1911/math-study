"""2019 고3 3월모의고사 나형 22번 — 파라미터 솔버 (수동 작성).
문제: a = 9^11 일 때 1/log_a(3). (답 22)
구조: 1/log_a(3) = log_3(a) = log_3(9^11) = log_3(3^22) = 22.
재생산: (밑 9, 지수 11, 진수 3) 파라미터화.
"""
import sympy as sp


def solve(a, inner):
    # 1/log_a(inner) = log_inner(a) = ln(a)/ln(inner)
    return sp.simplify(sp.log(a) / sp.log(inner))


CANDIDATE = 22
assert solve(sp.Integer(9) ** 11, 3) == CANDIDATE, solve(sp.Integer(9) ** 11, 3)
print('VERIFY_PASS')
