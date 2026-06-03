import math
from decimal import Decimal, getcontext
getcontext().prec = 50

# 구한 답
cos_theta = -math.sqrt(5) / 5
sin_theta = 2 * math.sqrt(5) / 5

# 원래 조건식 검증: sin(theta) = 2*cos(pi - theta)
# cos(pi - theta) = -cos(theta)
cos_pi_minus_theta = -cos_theta
sin_check = 2 * cos_pi_minus_theta

# sin(theta) 검증
if abs(sin_theta - sin_check) < 1e-10:
    condition_pass = True
else:
    condition_pass = False

# 기본 항등식 검증: sin^2(theta) + cos^2(theta) = 1
identity_check = sin_theta**2 + cos_theta**2
if abs(identity_check - 1.0) < 1e-10:
    identity_pass = True
else:
    identity_pass = False

# 최종 답 계산
tan_theta = sin_theta / cos_theta
result = cos_theta * tan_theta

# 기대값
expected = 2 * math.sqrt(5) / 5

if condition_pass and identity_pass and abs(result - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')