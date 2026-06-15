import sympy as sp
t = sp.Symbol('t', positive=True)
x = t**2 + sp.ln(t)
y = t**3 + 6*t
dx_dt = sp.diff(x, t)
dy_dt = sp.diff(y, t)
dy_dx = dy_dt / dx_dt
result = dy_dx.subs(t, 1)
if result == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')