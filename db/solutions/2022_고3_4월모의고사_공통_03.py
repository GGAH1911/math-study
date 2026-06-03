import sympy as sp
x = sp.Symbol('x')
expr = (sp.sqrt(2*x - 5) - 1) / (x - 3)
limit_result = sp.limit(expr, x, 3)
if limit_result == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')