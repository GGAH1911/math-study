import numpy as np
from math import tan, pi

# 구한 a, b 값
a = 1/4
b = 2

# 조건 1: 점 (0, 2)를 지나는가?
y_at_0 = tan(a * 0) + b
if abs(y_at_0 - 2) < 1e-9:
    cond1 = True
else:
    cond1 = False

# 조건 2: x = -2π, 2π, 6π에서 점근선을 가지는가?
# tan(ax) = tan(π/2 + nπ)에서 점근선 발생
# ax = π/2 + nπ ⟹ x = π/(2a) + nπ/a

asymptotes = []
for n in range(-2, 3):
    x_asym = pi/(2*a) + n*pi/a
    asymptotes.append(x_asym)

# 주어진 점근선들
given_asymptotes = [-2*pi, 2*pi, 6*pi]

# 계산된 점근선 중 주어진 점근선과 일치하는지 확인
matches = 0
for given in given_asymptotes:
    for calc in asymptotes:
        if abs(given - calc) < 1e-9:
            matches += 1
            break

cond2 = (matches == 3)

if cond1 and cond2:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')