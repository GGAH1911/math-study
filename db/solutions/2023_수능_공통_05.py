import math
from math import sqrt, cos, sin, tan, pi

# 주어진 조건 검증
sin_theta = -sqrt(5)/5
cos_theta = 2*sqrt(5)/5

# 검증 1: sin²θ + cos²θ = 1
check1 = abs(sin_theta**2 + cos_theta**2 - 1) < 1e-10

# 검증 2: tan θ < 0
tan_theta = sin_theta / cos_theta
check2 = tan_theta < 0

# 검증 3: cos(π/2 + θ) = √5/5
cos_result = -sin_theta
check3 = abs(cos_result - sqrt(5)/5) < 1e-10

if check1 and check2 and check3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')