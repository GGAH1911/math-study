import numpy as np
from math import sqrt

# 점들의 좌표
O = np.array([0, 0])
A = np.array([2, 0])
B = np.array([0, 2])

# 점 C의 좌표 (AC = 1 조건)
cos_theta = 7/8
sin_theta = sqrt(15)/8
C = np.array([2*cos_theta, 2*sin_theta])

# AC 거리 검증
AC_dist = np.linalg.norm(C - A)
assert abs(AC_dist - 1.0) < 1e-10, f'AC 거리 오류: {AC_dist}'

# 점 D: OC 위의 점, OD = 4/3
OD_length = 4/3
C_length = np.linalg.norm(C)
t = OD_length / C_length
D = t * C

# 삼각형 BOD의 넓이 계산
vec_OB = B - O
vec_OD = D - O
cross_product = vec_OB[0] * vec_OD[1] - vec_OB[1] * vec_OD[0]
area_BOD = abs(cross_product) / 2

# 조건 검증: 넓이 = 7/6
assert abs(area_BOD - 7/6) < 1e-10, f'삼각형 BOD 넓이 오류: {area_BOD}'

print('VERIFY_PASS')