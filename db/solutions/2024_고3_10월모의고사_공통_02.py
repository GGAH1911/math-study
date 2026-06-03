import sympy as sp
x = sp.Symbol('x')
f = x**3 - 2*x**2 - 4*x
limit_expr = (f + 5) / (x - 1)
result = sp.limit(limit_expr, x, 1)
if result == -5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')