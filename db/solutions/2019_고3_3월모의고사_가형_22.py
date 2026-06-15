"""2019 고3 3월모의고사 가형 22번 — 파라미터 솔버 (수동 작성).
문제: f(x)=e^{3x-3}+1 일 때 f'(1). (답 3)
구조: f(x)=e^{a x - a}+c → f'(x)=a·e^{a x-a}, f'(1)=a·e^0=a.
재생산: (a, c) 파라미터를 바꾸면 같은 유형 무한 생성, 답은 항상 a.
"""
import sympy as sp


def solve(a, c):
    x = sp.symbols('x')
    f = sp.exp(a * x - a) + c
    return sp.diff(f, x).subs(x, 1)


CANDIDATE = 3
assert solve(3, 1) == CANDIDATE, solve(3, 1)
print('VERIFY_PASS')
