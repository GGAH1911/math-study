import sympy as sp
x = sp.Symbol('x')
y = x**3 + x**2 - 5
dy_dx = sp.diff(y, x)
slope_at_1 = dy_dx.subs(x, 1)
print('VERIFY_PASS' if slope_at_1 == 5 else 'VERIFY_FAIL')