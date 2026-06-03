import sympy as sp

t = sp.Symbol('t', real=True)

# 원래 매개변수 방정식
x = 5*t / (t**2 + 1)
y = 3 * sp.ln(t**2 + 1)

# 도함수 계산
dx_dt = sp.diff(x, t)
dy_dt = sp.diff(y, t)

# dy/dx
dy_dx = dy_dt / dx_dt

# t=2일 때의 값
result = dy_dx.subs(t, 2)
result_simplified = sp.simplify(result)

if result_simplified == -4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')