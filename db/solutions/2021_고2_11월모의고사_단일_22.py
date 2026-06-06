import sympy as sp
x = sp.Symbol('x')
f = (9*x**2 + 1) / (3*x**2 + 5*x)
limit_value = sp.limit(f, x, -sp.oo)
if limit_value == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')