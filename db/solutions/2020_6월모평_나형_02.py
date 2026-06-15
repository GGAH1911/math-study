import sympy as sp
from sympy import sqrt, limit, oo, symbols

n = symbols('n', positive=True)
expr = sqrt(9*n**2 + 4*n + 1) / (2*n + 5)
result = limit(expr, n, oo)
expected = sp.Rational(3, 2)

if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')