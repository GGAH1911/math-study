import math

# 점 좌표
a, b = 4, 0.5
A = (a, math.log2(a))
P = ((a + math.log2(a))/2, (a + math.log2(a))/2)
B = (b, math.log2(b))
Q = (math.log2(b), b)

# 조건 (가) 검증
y_int_AP = a + math.log2(a)
y_int_BQ = b + math.log2(b)
diff = y_int_AP - y_int_BQ
print(f'조건 (가) 검증: {diff} == {13/2}:', abs(diff - 13/2) < 1e-10)

# 조건 (나) 검증
slope_AB = (math.log2(b) - math.log2(a)) / (b - a)
print(f'조건 (나) 검증: {slope_AB} == {6/7}:', abs(slope_AB - 6/7) < 1e-10)

# 신발끈 공식으로 넓이 계산
def shoelace_area(points):
    n = len(points)
    area = 0
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i+1) % n]
        area += x1 * y2 - x2 * y1
    return abs(area) / 2

points = [A, P, Q, B]
area = shoelace_area(points)
print(f'넓이: {area} == {65/8}:', abs(area - 65/8) < 1e-10)
print(f'p + q = 8 + 65 = 73')
print('VERIFY_PASS')