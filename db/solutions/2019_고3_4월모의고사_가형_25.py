"""2019 고3 4월모의고사 가형 25번 — 파라미터 솔버 (수동 작성).
문제: 곡선 y=(1/3)x³+2 ln x 의 변곡점에서의 접선의 기울기. (답 3)
구조: y''=2x-2/x²=0 → x³=1 → x=1 (변곡점). 기울기 y'(1)=x²+2/x |_{x=1}=1+2=3.
재생산: 계수 파라미터화.
"""
import sympy as sp


def solve(c3, c_ln):
    x = sp.symbols('x', positive=True)
    y = c3 * x ** 3 + c_ln * sp.ln(x)
    xinf = [r for r in sp.solve(sp.diff(y, x, 2), x) if r.is_real and r > 0][0]
    return sp.diff(y, x).subs(x, xinf)


CANDIDATE = 3
assert solve(sp.Rational(1, 3), 2) == CANDIDATE, solve(sp.Rational(1, 3), 2)
print('VERIFY_PASS')
