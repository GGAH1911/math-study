import sympy as sp
n = sp.Symbol('n')
expr = (2*n**2 + 3*n - 5) / (n**2 + 1)
limit_value = sp.limit(expr, n, sp.oo)
if limit_value == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')