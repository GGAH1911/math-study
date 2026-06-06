import numpy as np
import sympy as sp

# a = 24로 검증
a = 24
m = 1  # 임의의 양수

# 점들의 좌표 계산
x_A = np.sqrt(a / m)
y_A = m * x_A
x_B = x_A
y_B = -2 * a / x_A
x_C = x_A / 2
y_C = m * x_C
x_D = x_A / 2
y_D = -2 * a / x_D

# 각 점이 올바른 곡선 위에 있는지 검증
assert np.isclose(y_A, a / x_A), "A not on y=a/x"
assert np.isclose(y_A, m * x_A), "A not on y=mx"
assert np.isclose(y_B, -2 * a / x_B), "B not on y=-2a/x"
assert np.isclose(y_C, m * x_C), "C not on y=mx"
assert np.isclose(y_D, -2 * a / x_D), "D not on y=-2a/x"

# Shoelace 공식으로 넓이 계산
points = [(x_A, y_A), (x_C, y_C), (x_D, y_D), (x_B, y_B)]
area = 0
for i in range(len(points)):
    j = (i + 1) % len(points)
    area += points[i][0] * points[j][1] - points[j][0] * points[i][1]
area = abs(area) / 2

assert np.isclose(area, 45), f"Area {area} != 45"

# 대수적 검증
a_sym = sp.Symbol('a', positive=True)
m_sym = sp.Symbol('m', positive=True)
x_A_sym = sp.sqrt(a_sym / m_sym)
area_formula = 15 * a_sym / 8
a_solution = sp.solve(sp.Eq(area_formula, 45), a_sym)[0]
assert a_solution == 24, f"Algebraic solution {a_solution} != 24"

print('VERIFY_PASS')