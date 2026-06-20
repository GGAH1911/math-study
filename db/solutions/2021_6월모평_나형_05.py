from sympy import Rational
R = 15
sin_B = Rational(7, 10)
AC = 2 * R * sin_B
print('VERIFY_PASS' if AC == 21 else 'VERIFY_FAIL')