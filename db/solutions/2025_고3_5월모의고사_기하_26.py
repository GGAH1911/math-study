import numpy as np
from sympy import sqrt, simplify

# 쌍곡선 검증
a, b = 2, sqrt(5)
c = sqrt(a**2 + b**2)
assert simplify(c - 3) == 0, 'c should be 3'

# 점근선과 x=3의 교점
x_line = 3
y_P = (b/a) * x_line
y_Q = -(b/a) * x_line
assert simplify(y_P - 3*sqrt(5)/2) == 0, 'P y-coord mismatch'
assert simplify(y_Q + 3*sqrt(5)/2) == 0, 'Q y-coord mismatch'

# 삼각형 F'PQ의 넓이
F_prime = (-c, 0)
P = (x_line, y_P)
Q = (x_line, y_Q)

x1, y1 = float(-3), 0
x2, y2 = 3, float(3*sqrt(5)/2)
x3, y3 = 3, float(-3*sqrt(5)/2)

area_numerical = abs(x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2))/2
expected = float(9*sqrt(5))

assert abs(area_numerical - expected) < 1e-10, f'Area mismatch: {area_numerical} vs {expected}'

print('VERIFY_PASS')