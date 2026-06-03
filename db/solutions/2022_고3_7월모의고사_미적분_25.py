import sympy as sp
t = sp.Symbol('t', positive=True)
x = t**2 * sp.ln(t) + 3*t
y = 6*t*sp.exp(t - 1)
dx_dt = sp.diff(x, t)
dy_dt = sp.diff(y, t)
dydx = dy_dt / dx_dt
result = dydx.subs(t, 1)
result_simplified = sp.simplify(result)
if result_simplified == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', result_simplified)