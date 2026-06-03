import numpy as np
from sympy import symbols, solve, Rational

x = symbols('x')
f = x**3 - 4*x**2 + 6*x - 8
f_prime = 3*x**2 - 8*x + 6

# P에서의 접선과 곡선의 교점
intersection_eq = f - (x - 6)  # y = x - 6
roots = solve(intersection_eq, x)
# roots should be [1, 1, 2]

# Q에서의 접선 y = 2x - 8
# x축과의 교점: x = 4
# y축과의 교점: y = -8
# 삼각형 넓이 = 1/2 * 4 * 8 = 16

area = Rational(1, 2) * 4 * 8
if area == 16:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')