from scipy.integrate import quad
import numpy as np

CANDIDATE = 10

# 속도 함수
def v(t):
    return -4*t + 8

# v(t) = 0인 시점
t_zero = 2

# [0, 2] 구간의 변위
displacement_1, _ = quad(v, 0, 2)

# [2, 3] 구간의 변위
displacement_2, _ = quad(v, 2, 3)

# 움직인 거리 = |변위1| + |변위2|
total_distance = abs(displacement_1) + abs(displacement_2)

if abs(total_distance - CANDIDATE) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')