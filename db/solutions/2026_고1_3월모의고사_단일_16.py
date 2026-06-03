import math
from math import sqrt

# 정육각형 ABCDEF의 꼭짓점
A = (0, 0)
B = (1, 0)
C = (3/2, sqrt(3)/2)
D = (1, sqrt(3))
E = (0, sqrt(3))
F = (-1/2, sqrt(3)/2)

# ∠BAG = 45°이고 |AG| = 1
G = (sqrt(2)/2, sqrt(2)/2)

# 신발끈 공식으로 사각형 AGEF의 넓이
def shoelace_area(points):
    n = len(points)
    area = 0
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i+1) % n]
        area += x1*y2 - x2*y1
    return abs(area) / 2

quad_AGEF = [A, G, E, F]
area_calculated = shoelace_area(quad_AGEF)

# 정답값
area_expected = (sqrt(3) + sqrt(6)) / 4

# 검증
if abs(area_calculated - area_expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'Calculated: {area_calculated}')
    print(f'Expected: {area_expected}')