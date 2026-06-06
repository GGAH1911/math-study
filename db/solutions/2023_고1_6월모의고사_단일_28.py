import sympy as sp
from fractions import Fraction

# 원래 함수
def parabola(x):
    return x**2 - 4*x + 25/4

def line_oa(x):
    return x  # y = x

# 점 A
A_x = 5/2
A_y = A_x  # 직선 y = x 위의 점
assert abs(parabola(A_x) - A_y) < 1e-10

# 점 B (y축 교점)
B_x, B_y = 0, 25/4
assert abs(parabola(B_x) - B_y) < 1e-10

# 점 H (A에서 x축에 내린 수선의 발)
H_x, H_y = 5/2, 0

# 직선 BH의 방정식
# (y - B_y) / (x - B_x) = (H_y - B_y) / (H_x - B_x)
slope_BH = (H_y - B_y) / (H_x - B_x)
# y = slope_BH * (x - B_x) + B_y

# 점 C (직선 OA와 BH의 교점)
# y = x = slope_BH * (x - 0) + 25/4
# x = slope_BH * x + 25/4
# x - slope_BH * x = 25/4
# x(1 - slope_BH) = 25/4
C_x = (25/4) / (1 - slope_BH)
C_y = C_x

# 선분 BH 위의 점인지 확인
assert abs(C_y - (slope_BH * C_x + 25/4)) < 1e-10

# 삼각형 BOC의 넓이
S1 = 0.5 * abs(B_y) * C_x

# 삼각형 ACH의 넓이
# A = (5/2, 5/2), C = (C_x, C_y), H = (5/2, 0)
# AH는 수직선, 길이 = 5/2
# C에서 직선 x = 5/2까지의 거리 = |5/2 - C_x|
AH_length = A_y - H_y
C_dist_to_AH = abs(A_x - C_x)
S2 = 0.5 * AH_length * C_dist_to_AH

# S1 - S2
diff = S1 - S2
frac = Fraction(diff).limit_denominator(1000)
p, q = frac.denominator, frac.numerator

if p * diff > 0 and q * diff > 0:
    answer = p + q
    if abs(S1 - S2 - Fraction(q, p)) < 1e-10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')