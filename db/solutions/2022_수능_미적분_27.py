import sympy as sp
from sympy import Symbol, ln, exp, sqrt, integrate, simplify, Rational, solve

t = Symbol('t', positive=True)
x = Symbol('x')
# 곡선 y=x^2 과 직선 y=t^2 x - ln t / 8 의 교점
roots = solve(x**2 - (t**2 * x - ln(t)/8), x)
A, B = roots
# 중점 P
Px = sp.simplify((A + B)/2)
Py = sp.simplify((A**2 + B**2)/2)
# 도함수
dx = sp.diff(Px, t)
dy = sp.diff(Py, t)
speed_sq = sp.simplify(dx**2 + dy**2)
speed = sp.sqrt(speed_sq)
speed = sp.simplify(speed)
# t=1..e 까지 호의 길이
dist = sp.integrate(speed, (t, 1, sp.E))
dist = sp.simplify(dist)
expected = sp.E**4/2 - Rational(3, 8)
if sp.simplify(dist - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', dist, expected)
