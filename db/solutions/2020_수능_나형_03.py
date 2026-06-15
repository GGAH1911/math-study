import sympy as sp
n = sp.Symbol('n')
expr = sp.sqrt(9*n**2 + 4) / (5*n - 2)
limit_value = sp.limit(expr, n, sp.oo)
if limit_value == sp.Rational(3, 5):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')