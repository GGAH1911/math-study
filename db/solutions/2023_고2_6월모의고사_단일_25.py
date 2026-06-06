import math
from math import cos, pi

# 원래 함수: f(x) = 4*cos(x + pi) + k
k = 7

# 점 (π/3, 5)가 그래프 위에 있는지 확인
x = pi / 3
y_expected = 5

f_x = 4 * cos(x + pi) + k

if abs(f_x - y_expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')