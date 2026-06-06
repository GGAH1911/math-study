from sympy import Rational, S
expr = S(3)**(-2) * S(9)**Rational(3,2)
result = expr
if result == 3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', result)