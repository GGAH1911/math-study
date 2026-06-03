import numpy as np
from sympy import symbols, solve, simplify

# 접점 (4, 1)에서의 접선
# 접선 방정식: 4x + 3y = 19

# 검증 1: 접점이 타원 위에 있는가?
x0, y0 = 4, 1
ellipse_check = x0**2 + 3*y0**2
print(f'타원 값 (=19): {ellipse_check}')
assert ellipse_check == 19

# 검증 2: 접점이 접선 위에 있는가?
line_check = 4*x0 + 3*y0
print(f'접선 값 (=19): {line_check}')
assert line_check == 19

# 검증 3: 원점에서 직선 4x + 3y - 19 = 0까지의 거리
from math import sqrt
dist = 19 / sqrt(16 + 9)
print(f'거리 (=3.8): {dist}')
expected_dist = 19 / 5
assert abs(dist - expected_dist) < 1e-10

# 검증 4: 직선이 타원에 접하는가? (중근 확인)
from sympy import symbols, expand
x = symbols('x')
# y = (19 - 4x)/3을 타원 방정식에 대입
y_expr = (19 - 4*x) / 3
ellipse_sub = x**2 + 3*y_expr**2 - 19
ellipse_expanded = expand(ellipse_sub)
print(f'타원 대입식: {ellipse_expanded}')
# 정리하면 (x-4)^2 = 0이므로 중근
from sympy import factor
factored = factor(3*ellipse_expanded)
print(f'인수분해: {factored}')

# 기울기
m = -4/3
print(f'기울기: {m}')

print('VERIFY_PASS')