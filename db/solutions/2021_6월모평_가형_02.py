import sympy as sp
n = sp.Symbol('n', positive=True, real=True)
expr = sp.sqrt(9*n**2 + 12*n) - 3*n
limit_result = sp.limit(expr, n, sp.oo)
if limit_result == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')