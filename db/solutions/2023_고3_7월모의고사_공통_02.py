import sympy as sp
h = sp.Symbol('h')
f = lambda x: x**3 - 7*x + 5
f2 = f(2)
f2h = f(2 + h)
limit_expr = (f2h - f2) / h
limit_val = sp.limit(limit_expr, h, 0)
if limit_val == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')