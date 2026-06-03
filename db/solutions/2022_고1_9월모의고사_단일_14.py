import math
from sympy import sqrt, simplify

# 원의 중심
center = (3, 2)
radius = sqrt(5)

# 직선: 2x - y + 8 = 0
# 점 (x0, y0)에서 ax + by + c = 0까지의 거리: |ax0 + by0 + c| / sqrt(a^2 + b^2)
a, b, c = 2, -1, 8

# 중심에서 직선까지의 거리
dist_center = abs(a * center[0] + b * center[1] + c) / math.sqrt(a**2 + b**2)
dist_center_exact = abs(2*3 - 2 + 8) / sqrt(5)

# 원 위의 점과 직선 사이 최단거리
min_distance = dist_center_exact - radius
min_distance_simplified = simplify(min_distance)

# 예상 답: 7*sqrt(5)/5
expected = 7*sqrt(5)/5

if simplify(min_distance_simplified - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')