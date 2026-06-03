from sympy import Rational, Integer
val = Integer(4)**Rational(1,3) * Integer(2)**Rational(1,3)
print('VERIFY_PASS' if val == 2 else 'VERIFY_FAIL')