import numpy as np
from sympy import *

CANDIDATE = pi

# 주어진 범위
x_vals = np.linspace(0, 2*np.pi - 0.001, 10000)

# 두 함수 정의
y1 = np.sin(x_vals)
y2 = np.cos(x_vals + np.pi/2) + 1

# 교점 찾기: sin(x) = -sin(x) + 1 => sin(x) = 0.5
x_sym = symbols('x', real=True)
eq = Eq(sin(x_sym), Rational(1,2))

# [0, 2π) 범위에서의 해
sol1 = pi/6
sol2 = 5*pi/6

# 교점 검증
for x_val in [sol1, sol2]:
    y_sin = sin(x_val)
    y_cos = cos(x_val + pi/2) + 1
    assert abs(float(y_sin - y_cos)) < 1e-10, f'교점 불일치: x={x_val}'

# 합 계산
sum_x = sol1 + sol2
assert sum_x == CANDIDATE, f'합이 맞지 않음: {sum_x} != {CANDIDATE}'

print('VERIFY_PASS')