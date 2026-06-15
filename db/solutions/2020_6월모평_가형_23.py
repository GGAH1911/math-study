from sympy import *

CANDIDATE = 7

# 주어진 조건
cos_theta = Rational(1, 7)

# sin^2 + cos^2 = 1 에서 sin_theta 구하기
sin_theta_squared = 1 - cos_theta**2
sin_theta = sqrt(sin_theta_squared)  # 양수로 선택

# csc(theta) * tan(theta) 계산
csc_theta = 1 / sin_theta
tan_theta = sin_theta / cos_theta
result = csc_theta * tan_theta

# 간단히 정리
result_simplified = simplify(result)

if result_simplified == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')