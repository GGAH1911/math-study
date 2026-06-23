from sympy import Rational, Integer

result = Integer(2)**Integer(-1) * Integer(16)**Rational(1, 2)
if result == 2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')