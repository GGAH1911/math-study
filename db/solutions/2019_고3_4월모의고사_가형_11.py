"""2019 고3 4월모의고사 가형 11번 — 파라미터 솔버 (수동 작성).
문제: f(x)=2^x/3, g(x)=2^x-2. y축 교점 A(=f(0)), B(=g(0)), 곡선 교점 C. 삼각형 ABC 넓이. (답 ② 2/3·log_2 3)
구조: A=(0,1/3), B=(0,-1) (둘 다 y축). C: 2^x/3=2^x-2 → 2^x=3 → x=log_2 3.
      AB(밑변)은 y축 위 길이 |1/3-(-1)|=4/3, 높이=C의 x좌표=log_2 3.
      넓이=½·(4/3)·log_2 3 = (2/3) log_2 3.
재생산: (분모 d, g의 상수 c) 파라미터화 — f=2^x/d, g=2^x-c.
"""
import sympy as sp


def solve(d, c):
    x = sp.symbols('x', real=True)
    f, g = 2 ** x / d, 2 ** x - c
    A, B = f.subs(x, 0), g.subs(x, 0)            # y축 교점
    xc = sp.solve(sp.Eq(f, g), x)[0]             # 두 곡선 교점의 x
    return sp.simplify(sp.Rational(1, 2) * sp.Abs(A - B) * xc)


CANDIDATE = sp.Rational(2, 3) * sp.log(3, 2)
assert sp.simplify(solve(3, 2) - CANDIDATE) == 0, solve(3, 2)
print('VERIFY_PASS')
