import numpy as np
from sympy import *

# 원의 조건
a = 5
radius = sqrt(10)
center_x, center_y = 5, 5

# k = 1/3
k = Rational(1, 3)

# 직선 y = kx (즉 kx - y = 0)에서 점 (5,5)까지의 거리
dist = abs(k * center_x - center_y) / sqrt(k**2 + 1)

# 반지름과 비교
verify_tangent = simplify(dist - radius)

if verify_tangent == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')