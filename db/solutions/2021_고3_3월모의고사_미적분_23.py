import sympy as sp
n = sp.Symbol('n')
expr = (10*n**3 - 1) / ((n+2)*(2*n**2 + 3))
limit_result = sp.limit(expr, n, sp.oo)
if limit_result == 5:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')