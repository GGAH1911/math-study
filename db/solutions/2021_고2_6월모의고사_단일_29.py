import math
from fractions import Fraction

# 주어진 조건
a_sq = Fraction(3, 7)
a = math.sqrt(3/7)

# 좌표 설정
A = (0, 0)
B = (a, 0)
D = (-a, a * math.sqrt(3))

# 원 중심
h = a / 2
k = 5 * a * math.sqrt(3) / 6

# 반지름 확인
radius_sq = h**2 + k**2
assert abs(radius_sq - 1.0) < 1e-10, f'Radius check failed: {radius_sq}'

# E는 BD를 3:4로 내분
E = ((4*B[0] + 3*D[0])/7, (4*B[1] + 3*D[1])/7)

# C = 4E (A, E, C 일직선, t=4)
C = (4*E[0], 4*E[1])

# C가 원 위에 있는지 확인
dist_sq = (C[0] - h)**2 + (C[1] - k)**2
assert abs(dist_sq - 1.0) < 1e-10, f'C on circle check failed: {dist_sq}'

# 신발끈 공식으로 넓이 계산
def shoelace(vertices):
    area = 0
    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i+1) % len(vertices)]
        area += x1*y2 - x2*y1
    return abs(area) / 2

area = shoelace([A, B, C, D])
area_over_sqrt3 = area / math.sqrt(3)

# 넓이 = (6/7)*sqrt(3) 확인
expected_ratio = 6/7
assert abs(area_over_sqrt3 - expected_ratio) < 1e-10, f'Area check failed: {area_over_sqrt3}'

# p=7, q=6 확인
p, q = 7, 6
assert math.gcd(p, q) == 1, 'p, q not coprime'
assert abs(q/p - expected_ratio) < 1e-10, 'q/p check failed'

print('VERIFY_PASS')