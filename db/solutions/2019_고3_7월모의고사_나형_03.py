import sympy as sp
n = sp.Symbol('n')
expr = (5*n**2 - n) / (2*n**2 + 1)
limit_val = sp.limit(expr, n, sp.oo)
if limit_val == sp.Rational(5, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')