import numpy as np
from sympy import symbols, solve, sqrt

# 원의 조건: (x-3)^2 + y^2 = 5
# 직선: y = (1/2)x + k, 즉 x - 2y + 2k = 0

k = 1

# 점 (3, 0)에서 직선 x - 2y + 2k = 0까지의 거리
dist = abs(3 - 2*0 + 2*k) / sqrt(1**2 + (-2)**2)
dist_value = float(dist)

# 반지름
radius = sqrt(5)
radius_value = float(radius)

# 검증
if abs(dist_value - radius_value) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')