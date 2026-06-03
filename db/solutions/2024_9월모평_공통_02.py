import sympy as sp
x = sp.Symbol('x')
f = 2*x**2 - x
limit_expr = (f - 1) / (x - 1)
limit_value = sp.limit(limit_expr, x, 1)
if limit_value == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')