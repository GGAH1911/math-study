import numpy as np
from math import cos, pi

# 주어진 범위 조건
x_min = pi/2
x_max = pi

# 답안: x = 2π/3
x = 2*pi/3

# 범위 확인
assert x_min <= x <= x_max, f"범위 조건 위반: {x_min} <= {x} <= {x_max}"

# 원래 방정식 cos(x) = -1/2 검증
result = cos(x)
target = -1/2

if abs(result - target) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')