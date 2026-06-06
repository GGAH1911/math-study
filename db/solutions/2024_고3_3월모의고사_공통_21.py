import sympy as sp
from sympy import log, exp, symbols, solve, pi, sqrt

# 주어진 조건들을 검증
a_squared = 13
a = sqrt(13)
x1, x2 = 2, 13
c = 17

# 점 A와 B의 좌표
y1 = -x1 + c
y2 = -x2 + c

# 검증 1: 점 A가 지수함수와 직선의 교점
exp_check_A = a**x1 + 2
line_check_A = -x1 + c
assert abs(float(exp_check_A) - float(line_check_A)) < 1e-9, f'Point A mismatch: {float(exp_check_A)} vs {float(line_check_A)}'

# 검증 2: 점 B가 로그함수와 직선의 교점
log_check_B = log(x2, a) + 2
line_check_B = -x2 + c
assert abs(float(log_check_B) - float(line_check_B)) < 1e-9, f'Point B mismatch: {float(log_check_B)} vs {float(line_check_B)}'

# 검증 3: 원의 중심의 y좌표
center_y = (y1 + y2) / 2
assert abs(center_y - 19/2) < 1e-9, f'Center y-coordinate mismatch: {center_y} vs {19/2}'

# 검증 4: 원의 넓이
AB_squared = (x2 - x1)**2 + (y2 - y1)**2
AB = sqrt(AB_squared)
radius = AB / 2
area = pi * radius**2
expected_area = 121 * pi / 2
assert abs(float(area) - float(expected_area)) < 1e-9, f'Area mismatch: {float(area)} vs {float(expected_area)}'

print('VERIFY_PASS')