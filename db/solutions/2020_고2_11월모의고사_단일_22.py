import sympy as sp
CANDIDATE = 8
x = sp.Symbol('x')
f = (x**2 + 6*x - 7) / (x - 1)
limit_result = sp.limit(f, x, 1)
if limit_result == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')