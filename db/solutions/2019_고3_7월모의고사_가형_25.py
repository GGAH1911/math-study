import sympy as sp

CANDIDATE = 8

t = sp.Symbol('t', positive=True, real=True)

# 주어진 함수
x = t + sp.ln(t)
y = sp.Rational(1,2)*t**2 + t

# 미분
dx_dt = sp.diff(x, t)
dy_dt = sp.diff(y, t)

# dx/dt = dy/dt 조건
equation = sp.Eq(dx_dt, dy_dt)
t_solution = sp.solve(equation, t)

# t=1에서 속도 성분
t_val = 1
v_x = dx_dt.subs(t, t_val)
v_y = dy_dt.subs(t, t_val)

# |v|^2 계산
v_squared = v_x**2 + v_y**2

if v_squared == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')