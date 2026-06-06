import numpy as np
from math import pi, cos, sin, sqrt

# 문제 조건
angle_A = pi / 3
R = 7
AC = sqrt(21)
AB = 3 * AC

# 정현법칙으로 BC 계산
BC = 2 * R * sin(angle_A)

# 코사인 법칙으로 검증: BC² = AB² + AC² - 2·AB·AC·cos(A)
BC_squared_from_law = AB**2 + AC**2 - 2*AB*AC*cos(angle_A)
BC_squared_calculated = BC**2

# 검증
if abs(BC_squared_from_law - BC_squared_calculated) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')