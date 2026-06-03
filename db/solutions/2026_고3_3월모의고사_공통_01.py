from sympy import *
import math

# 원래 문제식: 4^(2/3) × 2^(-1/3)
result = (4 ** Rational(2,3)) * (2 ** Rational(-1,3))
expected = 2

if simplify(result) == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')