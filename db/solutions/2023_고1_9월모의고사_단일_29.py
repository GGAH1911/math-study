import math
from fractions import Fraction

# 주어진 점
A = (-5, -1)
sqrt105 = math.sqrt(105)

# 구한 B, C의 좌표
xB = (5 - 2*sqrt105) / 5
yB = (10 + sqrt105) / 5
xC = (5 + 2*sqrt105) / 5
yC = (10 - sqrt105) / 5

B = (xB, yB)
C = (xC, yC)

# 조건 1: 무게중심이 (-1, 1)
Gx = (A[0] + B[0] + C[0]) / 3
Gy = (A[1] + B[1] + C[1]) / 3
assert abs(Gx - (-1)) < 1e-9 and abs(Gy - 1) < 1e-9, f"무게중심 오류: ({Gx}, {Gy})"

# 조건 2: 원점 중심, 모두 반지름 26 위
rA_sq = A[0]**2 + A[1]**2
rB_sq = B[0]**2 + B[1]**2
rC_sq = C[0]**2 + C[1]**2
assert abs(rA_sq - 26) < 1e-9, f"A 거리 오류: {rA_sq}"
assert abs(rB_sq - 26) < 1e-9, f"B 거리 오류: {rB_sq}"
assert abs(rC_sq - 26) < 1e-9, f"C 거리 오류: {rC_sq}"

# 넓이 계산
AB = (B[0] - A[0], B[1] - A[1])
AC = (C[0] - A[0], C[1] - A[1])
cross = AB[0] * AC[1] - AB[1] * AC[0]
area = abs(cross) / 2

# 넓이 = (12*sqrt(105)) / 5
expected_area = 12 * sqrt105 / 5
assert abs(area - expected_area) < 1e-9, f"넓이 오류: {area} vs {expected_area}"

# 답: p + q = 5 + 12 = 17
print("VERIFY_PASS")