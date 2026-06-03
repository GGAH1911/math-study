import sympy as sp
n = sp.Symbol('n')
expr = (2*n + 1) * (3*n - 1) / (n**2 + 1)
limit_result = sp.limit(expr, n, sp.oo)
if limit_result == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')