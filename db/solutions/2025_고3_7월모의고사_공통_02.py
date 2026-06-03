import sympy as sp
h = sp.Symbol('h')
f = lambda x: x**3 + x
f_1 = f(1)
f_1_plus_h = f(1 + h)
limit_expr = (f_1_plus_h - f_1) / h
result = sp.limit(limit_expr, h, 0)
if result == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')