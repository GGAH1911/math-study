import sympy as sp
x = sp.Symbol('x')
expr = (x**2 + x - 6) / (x - 2)
limit_value = sp.limit(expr, x, 2)
if limit_value == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')