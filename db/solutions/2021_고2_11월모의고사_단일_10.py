import math
from fractions import Fraction

# 점 P(4, -3)에서 원점까지의 거리
r = math.sqrt(4**2 + (-3)**2)
sin_theta = -3 / r
cos_theta = 4 / r

# sin(π/2 + θ) - sin(θ) 계산
result = math.sin(math.pi/2 + math.asin(sin_theta)) - sin_theta

# 또는 직접 계산: sin(π/2 + θ) = cos(θ)
result_direct = cos_theta - sin_theta

# 답: 7/5
expected = 7/5

if abs(result_direct - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')