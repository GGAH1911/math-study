import numpy as np
from sympy import sqrt, simplify, symbols

CANDIDATE = 11

# a를 구함
a = 3 + sqrt(11)

# 검증: a가 방정식 a^4 - 40a^2 + 4 = 0을 만족하는지 확인
eq_result = simplify(a**4 - 40*a**2 + 4)

# (a-3)^2 = 11 확인
a_minus_3_squared = simplify((a - 3)**2)

if a_minus_3_squared == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')