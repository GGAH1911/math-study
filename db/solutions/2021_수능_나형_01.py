from sympy import *
# 원래 문제의 식
result = 3**0 * 8**(Rational(2, 3))
print('VERIFY_PASS' if result == 4 else 'VERIFY_FAIL')