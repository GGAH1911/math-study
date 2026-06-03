import math

# 주어진 조건
sin_theta = 4/5

# cos(theta) 계산
cos_theta_squared = 1 - sin_theta**2
cos_theta = math.sqrt(cos_theta_squared)

# 원래 식으로 검증: sin(pi/2 - theta) - cos(pi + theta)
# sin(pi/2 - theta) = cos(theta)
# cos(pi + theta) = -cos(theta)
result = cos_theta - (-cos_theta)

expected = 6/5

if abs(result - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')