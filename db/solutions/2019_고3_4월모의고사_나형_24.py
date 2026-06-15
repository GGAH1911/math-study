"""2019 고3 4월모의고사 나형 24번 — 파라미터 솔버 (수동 작성).
문제: (ax+1)⁶ 전개식에서 x의 계수와 x³의 계수가 같을 때, 양수 a에 대하여 20a². (답 6)
구조: x계수=C(6,1)a=6a, x³계수=C(6,3)a³=20a³. 6a=20a³ → a²=3/10 → 20a²=6.
재생산: (지수 n, 배수) 파라미터화.
"""
import sympy as sp


def solve(n=6, mult=20):
    a, x = sp.symbols('a x', positive=True)
    e = sp.expand((a * x + 1) ** n)
    aval = [s for s in sp.solve(sp.Eq(e.coeff(x, 1), e.coeff(x, 3)), a) if s > 0][0]
    return mult * aval ** 2


CANDIDATE = 6
assert solve() == CANDIDATE, solve()
print('VERIFY_PASS')
