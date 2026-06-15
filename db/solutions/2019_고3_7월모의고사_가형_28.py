import math
from sympy import sqrt, symbols, solve, simplify

CANDIDATE = 18

# 쌍곡선 매개변수
a, b, c = 3, 4, 5
F = (5, 0)
Fp = (-5, 0)

# P의 좌표
x0 = 75/7
y0 = 96/7
P = (x0, y0)

# 쌍곡선 검증
hyperbola_check = (x0**2 / 9) - (y0**2 / 16)
assert abs(hyperbola_check - 1) < 1e-9, f"P가 쌍곡선 위에 있지 않음: {hyperbola_check}"

# 거리 계산
dist_PF = math.sqrt((x0 - F[0])**2 + (y0 - F[1])**2)
dist_PFp = math.sqrt((x0 - Fp[0])**2 + (y0 - Fp[1])**2)
dist_FFp = 10

# 쌍곡선 성질 확인
assert abs(dist_PFp - dist_PF - 6) < 1e-9, "쌍곡선 성질 위반"

# 삼각형 넓이
area = 5 * y0

# 삼각형 둘레
perimeter = dist_PF + dist_PFp + dist_FFp
s = perimeter / 2

# 내접원 반지름
inradius = area / s
assert abs(inradius - 3) < 1e-9, f"내접원 반지름이 3이 아님: {inradius}"

# 내접원의 중심
Q_x = (dist_FFp * x0 + dist_PF * Fp[0] + dist_PFp * F[0]) / perimeter
Q_y = (dist_FFp * y0 + dist_PF * Fp[1] + dist_PFp * F[1]) / perimeter
Q = (Q_x, Q_y)

# Q에서 세 변까지 거리 검증
# 변 1: FF' (y = 0)
dist_to_FFp = abs(Q_y)
assert abs(dist_to_FFp - 3) < 1e-9, f"FF'까지 거리: {dist_to_FFp}"

# 변 2: PF (직선 12x - 5y - 60 = 0)
dist_to_PF = abs(12*Q_x - 5*Q_y - 60) / math.sqrt(144 + 25)
assert abs(dist_to_PF - 3) < 1e-9, f"PF까지 거리: {dist_to_PF}"

# 변 3: PFp (직선 48x - 55y + 240 = 0)
dist_to_PFp = abs(48*Q_x - 55*Q_y + 240) / math.sqrt(2304 + 3025)
assert abs(dist_to_PFp - 3) < 1e-9, f"PFp까지 거리: {dist_to_PFp}"

# OQ^2 계산
OQ_squared = Q_x**2 + Q_y**2
assert abs(OQ_squared - CANDIDATE) < 1e-9, f"OQ^2 = {OQ_squared}, 예상값 = {CANDIDATE}"

print('VERIFY_PASS')