import math

# 주어진 조건으로 좌표 설정
AD = 7/2
BC = AD + 3/2  # = 5
CD = 4

# 꼭짓점 좌표
A = (-AD, 0)
B = (-(AD + 3/2), -4)
C = (0, -4)
D = (0, 0)

# 신발끈 공식으로 넓이 계산
def shoelace_area(vertices):
    n = len(vertices)
    area = 0
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    return abs(area) / 2

vertices = [A, B, C, D]
area = shoelace_area(vertices)

# 검증: 넓이가 17이어야 함
if abs(area - 17) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')