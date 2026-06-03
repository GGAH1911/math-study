import sympy as sp
t = sp.Symbol('t')
x = sp.exp(t) + 2*t
y = sp.exp(-t) + 3*t
dx_dt = sp.diff(x, t)
dy_dt = sp.diff(y, t)
x_0 = x.subs(t, 0)
y_0 = y.subs(t, 0)
slope = (dy_dt.subs(t, 0)) / (dx_dt.subs(t, 0))
a = slope * (10 - x_0) + y_0
if abs(float(a) - 7.0) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')