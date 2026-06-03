import math
from math import sqrt

# 쌍곡선 쌍곡선 x²/a² - y²/b² = 1
a = 2
b = sqrt(5)

# 점근선: y = (b/a)x 또는 sqrt(5)x - 2y = 0
# 점 F(3, 0)에서 직선 sqrt(5)x - 2y = 0까지의 거리

# 직선의 일반형: Ax + By + C = 0에서 sqrt(5)x - 2y + 0 = 0
A = sqrt(5)
B = -2
C = 0

# 점 (x0, y0) = (3, 0)에서 거리
x0, y0 = 3, 0
distance = abs(A*x0 + B*y0 + C) / sqrt(A**2 + B**2)

expected_answer = sqrt(5)

if abs(distance - expected_answer) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')