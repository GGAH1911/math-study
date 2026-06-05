import sympy as sp
n = sp.Symbol('n')
expr = (2**n + 3**(n+1)) / (3**n + 1)
limit_result = sp.limit(expr, n, sp.oo)
print('VERIFY_PASS' if limit_result == 3 else f'VERIFY_FAIL: {limit_result}')