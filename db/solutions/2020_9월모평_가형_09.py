import math
from sympy import *

# 주어진 조건
cos_theta = Rational(-3, 5)

# sin(theta) 계산
sin_theta_squared = 1 - cos_theta**2
sin_theta = sqrt(sin_theta_squared)  # 제2사분면이므로 양수

# sin(pi + theta) = -sin(theta)
sin_pi_plus_theta = -sin_theta

# csc(pi + theta) = 1 / sin(pi + theta)
csc_pi_plus_theta = 1 / sin_pi_plus_theta

# 결과 검증
result = csc_pi_plus_theta
expected = Rational(-5, 4)

if result == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')