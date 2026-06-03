import numpy as np
from sympy import *

sin_theta = Rational(-1, 2)
cos_theta = sqrt(3) / 2
tan_theta = -sqrt(3) / 3

# 검증 1: 기본 항등식
check1 = sin_theta**2 + cos_theta**2
assert simplify(check1 - 1) == 0, f'sin²+cos²=1 실패: {check1}'

# 검증 2: tan 정의
check2 = sin_theta / cos_theta
assert simplify(check2 - tan_theta) == 0, f'tan 정의 실패: {check2}'

# 검증 3: 주어진 조건식
result = sin_theta + cos_theta * tan_theta
assert simplify(result) == -1, f'조건식 실패: {result}'

print('VERIFY_PASS')