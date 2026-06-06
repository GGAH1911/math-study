import numpy as np
from scipy.optimize import fsolve

# 원래 문제의 조건
k = 8

# 점들의 좌표
A = np.array([2, 0])
D = np.array([0, k/2])
C = np.array([-k, 0])
B = np.array([0, -1])

# Shoelace 공식으로 넓이 계산
points = np.array([A, D, C, B])
area = 0.5 * abs(sum(points[i][0] * points[(i+1)%4][1] - points[(i+1)%4][0] * points[i][1] for i in range(4)))
print(f'사각형 넓이: {area}')

# 두 직선 사이의 거리 계산
# l1: x - 2y - 2 = 0
# l2: x - 2y + 8 = 0
dist = abs(-2 - 8) / np.sqrt(1**2 + 2**2)
print(f'd = {dist}')
print(f'd^2 = {dist**2}')

# 검증: 사각형 넓이가 25인지 확인
if abs(area - 25) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')