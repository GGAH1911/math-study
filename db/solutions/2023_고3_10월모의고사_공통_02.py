import sympy as sp
h = sp.Symbol('h')
f = lambda x: 2*x**3 + 3*x
f_0 = f(0)
f_2h = f(2*h)
limit_expr = (f_2h - f_0) / h
result = sp.limit(limit_expr, h, 0)
if result == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')