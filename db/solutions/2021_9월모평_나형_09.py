import math
from math import sin, cos, pi, sqrt

# 주어진 값
AB = 8
angle_A = 45 * pi / 180
angle_B = 15 * pi / 180
angle_C = 120 * pi / 180

# 정현법칙: BC/sin(A) = AB/sin(C)
BC = AB * sin(angle_A) / sin(angle_C)

# 예상 답
expected = 8 * sqrt(6) / 3

# 검증
if abs(BC - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')