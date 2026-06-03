from sympy import *
n = symbols('n')
expr = sqrt(4*n**2 + 3*n) - sqrt(4*n**2 + 1)
limit_value = limit(expr, n, oo)
if limit_value == Rational(3, 4):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')