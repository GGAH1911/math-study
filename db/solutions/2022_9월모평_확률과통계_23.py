from sympy import Rational
n = 60
p = Rational(1, 4)
E_X = n * p
print('VERIFY_PASS' if E_X == 15 else 'VERIFY_FAIL')