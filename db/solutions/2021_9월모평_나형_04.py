import sympy as sp
x = sp.Symbol('x')
expr = (x**2 + 9*x + 8) / (x + 1)
limit_value = sp.limit(expr, x, -1)
if limit_value == 7:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')