import sympy as sp
from sympy import sqrt, symbols, simplify, Rational

CANDIDATE = Rational(1, 8)

t = symbols('t', positive=True, real=True)

# 매개변수 함수
x = t**2 + 1
y = 4*sqrt(t)

# 미분
dx_dt = sp.diff(x, t)
dy_dt = sp.diff(y, t)

# dy/dx
dy_dx = dy_dt / dx_dt

# t=4에서의 값
dy_dx_at_4 = dy_dx.subs(t, 4)
dy_dx_simplified = simplify(dy_dx_at_4)

# 검증
if dy_dx_simplified == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')