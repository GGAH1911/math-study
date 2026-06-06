import math
from sympy import *

theta = Rational(5, 6) * pi

cos_val = cos(theta)
sin_val = sin(theta)

# 원래 문제의 조건 확인
expected_cos = Rational(-1, 2) * sqrt(3)

# sin^2 + cos^2 = 1 검증
identity_check = simplify(sin_val**2 + cos_val**2)

if cos_val == expected_cos and sin_val == Rational(1, 2) and identity_check == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')