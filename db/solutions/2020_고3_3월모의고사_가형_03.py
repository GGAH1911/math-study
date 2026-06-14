from sympy import sqrt, limit, Symbol, oo
n = Symbol('n', positive=True)
expr = sqrt(4*n**2 + 2*n + 1) - sqrt(4*n**2 - 2*n - 1)
result = limit(expr, n, oo)
if result == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')