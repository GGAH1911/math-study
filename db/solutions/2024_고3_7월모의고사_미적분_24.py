import math
from sympy import symbols, exp, diff, simplify

t = symbols('t', real=True, positive=True)
x = 3*t - 1/t
y = t*exp(t-1)

# 미분계수 계산
dx_dt = diff(x, t)
dy_dt = diff(y, t)

# t=1에서의 값
dx_dt_at_1 = float(dx_dt.subs(t, 1))
dy_dt_at_1 = float(dy_dt.subs(t, 1))

# dy/dx 계산
dy_dx_at_1 = dy_dt_at_1 / dx_dt_at_1

# 검증: 답은 1/2 = 0.5
expected = 0.5
if abs(dy_dx_at_1 - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')