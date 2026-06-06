from sympy import *
x = cbrt(9) * 3**(Rational(1, 3))
result = simplify(x)
expected = 3
if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')