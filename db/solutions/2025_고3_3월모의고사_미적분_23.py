import sympy as sp
n = sp.Symbol('n', positive=True)
expr = (n**2 - n + 2) / (4*n**2 - 1)
result = sp.limit(expr, n, sp.oo)
if result == sp.Rational(1, 4):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')