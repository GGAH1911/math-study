import sympy as sp
from sympy import sqrt, symbols, solve

m = sp.Rational(4, 3)
a_val = (2 + 2*sqrt(m**2 + 1)) / m

# 원의 중심과 반지름
center = (a_val, 2)
radius = 2

# P: x축과의 접점
P = (a_val, 0)

# Q: 직선 y=mx와의 접점
Q_x = a_val - 2*m / sqrt(m**2 + 1)
Q_y = 2 + 2 / sqrt(m**2 + 1)
Q = (Q_x, Q_y)

# Q가 직선 위에 있는지 확인
verify_on_line = sp.simplify(Q_y - m*Q_x)
assert verify_on_line == 0, f"Q not on line: {verify_on_line}"

# 중심에서 직선까지 거리 = 2
dist = abs(m*a_val - 2) / sqrt(m**2 + 1)
assert sp.simplify(dist - radius) == 0, f"Distance check failed: {dist}"

# R: y축과의 교점
R_y = a_val * (sqrt(m**2 + 1) + 1) / m
R = (0, R_y)

# 삼각형 ROP의 넓이
area = sp.Rational(1, 2) * a_val * R_y
assert area == 16, f"Area check failed: {area}"

print('VERIFY_PASS')