from sympy import Rational
a1 = Rational(2)
r = Rational(5)
a2 = a1 * r**(2-1)
CANDIDATE = 10
print('VERIFY_PASS' if a2 == CANDIDATE else 'VERIFY_FAIL')