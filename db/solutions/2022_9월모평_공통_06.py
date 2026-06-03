import math

# 주어진 조건: cos(theta) = -sqrt(3)/3
cos_theta = -math.sqrt(3)/3
cos_sq = cos_theta**2
sin_sq = 1 - cos_sq
sin_theta = math.sqrt(sin_sq)  # 범위에서 sin(theta) > 0

# 원래 조건식 검증: sin(theta)/(1-sin(theta)) - sin(theta)/(1+sin(theta)) = 4
lhs = sin_theta/(1-sin_theta) - sin_theta/(1+sin_theta)

if abs(lhs - 4) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')