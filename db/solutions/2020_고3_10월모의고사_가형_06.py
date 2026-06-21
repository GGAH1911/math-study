import sympy as sp
t = sp.Symbol('t', positive=True, real=True)
x = t**2 + 1
y = 4*sp.sqrt(t)
dx_dt = sp.diff(x, t)
dy_dt = sp.diff(y, t)
dy_dx = dy_dt / dx_dt
result = dy_dx.subs(t, 4)
expected = sp.Rational(1, 8)
if sp.simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')