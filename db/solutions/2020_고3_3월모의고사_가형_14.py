from sympy import log, simplify, Rational
import math

# 교점
A_x, B_x = -1, 3
A_y = log(2, 3)  # log_3(2)
B_y = log(6, 3)  # log_3(6)

# AB의 기울기
slope_AB = (B_y - A_y) / (B_x - A_x)
assert simplify(slope_AB) == Rational(1, 4), f'slope_AB should be 1/4, got {slope_AB}'

# 수직선 기울기
slope_perp = -4

# AB의 중점
M_x = (A_x + B_x) / 2
M_y = (A_y + B_y) / 2

# C의 y좌표 (y축과의 교점)
C_y = M_y - slope_perp * M_x
C_y_simplified = simplify(C_y)

# 삼각형 넓이 공식: 1/2 * |x_A(y_B - y_C) + x_B(y_C - y_A)|
area_expr = abs(A_x * (B_y - C_y) + B_x * (C_y - A_y)) / 2
area_simplified = simplify(area_expr)

# 수치 검증
area_numeric = float(area_simplified)
expected = 17 / 2

if abs(area_numeric - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {area_numeric}, expected {expected}')