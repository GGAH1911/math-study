from sympy import Rational

# 답: a = 6/7
a = Rational(6, 7)

# 점 A: (2, a/2)
A = (2, a / 2)
# 점 B: (a/2, 2)
B = (a / 2, 2)

# 곡선 위에 있는지 확인
assert A[1] == a / A[0], f'A not on curve'
assert B[1] == a / B[0], f'B not on curve'

# A의 y좌표 < 2
assert A[1] < 2, f'A y-coord must be < 2'

# 사각형 OACB의 넓이 (Shoelace)
verts = [(0, 0), A, (2, 2), B]
area = 0
for i in range(len(verts)):
    j = (i + 1) % len(verts)
    area += verts[i][0] * verts[j][1] - verts[j][0] * verts[i][1]
area = abs(area) / 2

expected = Rational(22, 7)
assert area == expected, f'Area {area} != {expected}'

print('VERIFY_PASS')