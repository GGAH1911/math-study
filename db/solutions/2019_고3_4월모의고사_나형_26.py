"""2019 고3 4월모의고사 나형 26번 — 파라미터 솔버 (수동 작성).
문제: lim_{x→∞} a x²/(x²-1)=2, lim_{x→1} a(x-1)/(x²-1)=b 일 때 a+b. (답 3)
구조: 첫 극한 = a = 2 → a=2. 둘째 극한 = lim_{x→1} a/(x+1) = a/2 = 1 = b. → a+b = 3.
재생산: 극한값 파라미터화.
"""
import sympy as sp


def solve():
    x, a = sp.symbols('x a')
    a_val = sp.solve(sp.Eq(sp.limit(a * x ** 2 / (x ** 2 - 1), x, sp.oo), 2), a)[0]
    b_val = sp.limit(a_val * (x - 1) / (x ** 2 - 1), x, 1)
    return a_val + b_val


CANDIDATE = 3
assert solve() == CANDIDATE, solve()
print('VERIFY_PASS')
