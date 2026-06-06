import math
from math import sin, pi

# 원래 함수: y = 2*sin(x - pi/3) + k
# 점 (pi/6, 2)를 지남

k = 3
x = pi / 6
y_expected = 2

# 함수 계산
y_calculated = 2 * sin(x - pi/3) + k

# 검증
if abs(y_calculated - y_expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')