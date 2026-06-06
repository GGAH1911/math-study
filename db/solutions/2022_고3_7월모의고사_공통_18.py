import sympy as sp
a_val = 16
t = sp.Symbol('t')
v = 3*t**2 + 6*t - a_val
x = sp.integrate(v, t)
x_at_0 = x.subs(t, 0)
x_func = x - x_at_0
x_at_3 = x_func.subs(t, 3)
if x_at_3 == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')