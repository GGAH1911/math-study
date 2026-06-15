"""2019 고3 3월모의고사 가형 23번 — 파라미터 솔버 (수동 작성).
문제: (2x + 1/2)^6 전개식에서 x^4 의 계수. (답 60)
구조: 이항정리 — (a x + b)^n 에서 x^p 계수 = C(n,p) a^p b^{n-p}.
      여기 C(6,4)·2^4·(1/2)^2 = 15·16·(1/4) = 60.
재생산: (a,b,n,power) 파라미터화 → 같은 유형 무한 생성.
"""
import sympy as sp


def coeff(a, b, n, power):
    x = sp.symbols('x')
    return sp.expand((a * x + b) ** n).coeff(x, power)


CANDIDATE = 60
assert coeff(2, sp.Rational(1, 2), 6, 4) == CANDIDATE, coeff(2, sp.Rational(1, 2), 6, 4)
print('VERIFY_PASS')
