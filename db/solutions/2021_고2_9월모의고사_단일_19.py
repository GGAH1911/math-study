import math
from fractions import Fraction

# 조건: 4*sin(theta) = 3*cos(theta)
sin_theta = Fraction(3, 5)
cos_theta = Fraction(4, 5)

sin_2theta = 2 * sin_theta * cos_theta
cos_2theta = cos_theta**2 - sin_theta**2

P = (5 * cos_2theta, 5 * sin_2theta)
A = (Fraction(-5), Fraction(0))
B = (Fraction(5), Fraction(0))
O = (Fraction(0), Fraction(0))

# |PA| 검증
PA_dist_sq = (P[0] - A[0])**2 + (P[1] - A[1])**2
assert PA_dist_sq == 64, f'|PA|^2 = {PA_dist_sq}, expected 64'

# 점 C: 선분 PB 연장선, |PC| = 8
PB = (B[0] - P[0], B[1] - P[1])
PB_dist_sq = PB[0]**2 + PB[1]**2
t_C = Fraction(8, 1) / math.sqrt(float(PB_dist_sq))
C = (P[0] + Fraction(4, 3) * PB[0], P[1] + Fraction(4, 3) * PB[1])

# |PC| 검증
PC_dist_sq = (C[0] - P[0])**2 + (C[1] - P[1])**2
assert PC_dist_sq == 64, f'|PC|^2 = {PC_dist_sq}'

# 점 D: 선분 PO 연장선, |PD| = 8
PO = (O[0] - P[0], O[1] - P[1])
D = (P[0] + Fraction(8, 5) * PO[0], P[1] + Fraction(8, 5) * PO[1])

# |PD| 검증
PD_dist_sq = (D[0] - P[0])**2 + (D[1] - P[1])**2
assert PD_dist_sq == 64, f'|PD|^2 = {PD_dist_sq}'

# 넓이 계산
x1, y1 = A
x2, y2 = D
x3, y3 = C
area = abs(x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2)) / 2

expected = Fraction(64, 5)
assert area == expected, f'Area = {area}, expected {expected}'

print('VERIFY_PASS')