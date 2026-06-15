from sympy import Rational, Integer
result = Integer(16) * Integer(2)**(-3)
expected = 2
if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')