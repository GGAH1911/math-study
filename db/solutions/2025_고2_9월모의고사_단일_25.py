import math
from math import sqrt

# 주어진 값
AB = 8
BC = 12
sin_B = sqrt(15) / 4
cos_B = -1/4

# 검증 1: 넓이 확인
area = 0.5 * AB * BC * sin_B
expected_area = 12 * sqrt(15)
area_check = abs(area - expected_area) < 1e-10

# 검증 2: sin^2 + cos^2 = 1
trig_identity = abs(sin_B**2 + cos_B**2 - 1) < 1e-10

# 검증 3: AC 계산 및 확인
AC_squared = AB**2 + BC**2 - 2*AB*BC*cos_B
AC = sqrt(AC_squared)
AC_check = abs(AC - 16) < 1e-10

# 검증 4: 삼각형 부등식 확인
triangle_inequality = (AB + BC > AC) and (AB + AC > BC) and (BC + AC > AB)

if area_check and trig_identity and AC_check and triangle_inequality:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')