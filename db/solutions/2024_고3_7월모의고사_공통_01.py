from sympy import *
a = Rational(4, 3)
b = Rational(-1, 3)
result = 2**a * 2**b
expected = 2
if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')