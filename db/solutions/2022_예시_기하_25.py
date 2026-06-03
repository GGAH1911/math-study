from sympy import *
import numpy as np

# 좌표 설정
A = np.array([3, 0, 4])
B = np.array([0, 4, 0])
C = np.array([0, 4, 8])

# 조건 검증
# 1. AP = 4 확인
P = np.array([3, 0, 0])
AP_dist = np.linalg.norm(A - P)
assert abs(AP_dist - 4) < 1e-10, f'AP = {AP_dist} (should be 4)'

# 2. PQ = 3 확인
Q = np.array([0, 0, 0])
PQ_dist = np.linalg.norm(P - Q)
assert abs(PQ_dist - 3) < 1e-10, f'PQ = {PQ_dist} (should be 3)'

# 3. QB = 4 확인
QB_dist = np.linalg.norm(B - Q)
assert abs(QB_dist - 4) < 1e-10, f'QB = {QB_dist} (should be 4)'

# 4. AB = AC 확인
AB_dist = np.linalg.norm(B - A)
AC_dist = np.linalg.norm(C - A)
assert abs(AB_dist - AC_dist) < 1e-10, f'AB = {AB_dist}, AC = {AC_dist} (should be equal)'

# 넓이 계산
vec_AB = B - A
vec_AC = C - A
cross_product = np.cross(vec_AB, vec_AC)
area = 0.5 * np.linalg.norm(cross_product)

if abs(area - 20) < 1e-10:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: area = {area}')