import numpy as np
from scipy.optimize import fsolve

# 좌표 설정
A = np.array([0, 0, 0])
B = np.array([0, 0, 4])
C = np.array([8, 0, 0])
D = np.array([4, 4*np.sqrt(3), 0])

# 검증: 거리 조건
assert abs(np.linalg.norm(B - A) - 4) < 1e-10, 'AB=4 검증 실패'
assert abs(np.linalg.norm(D - C) - 8) < 1e-10, 'CD=8 검증 실패'
assert abs(np.linalg.norm(C - B) - 4*np.sqrt(5)) < 1e-10, 'BC 검증 실패'
assert abs(np.linalg.norm(D - B) - 4*np.sqrt(5)) < 1e-10, 'BD 검증 실패'

# M, N, P
M = (C + D) / 2
N = (D + B) / 2
P = np.array([3, np.sqrt(3), 0])

# DB ⊥ PN 검증
DB = B - D
PN = N - P
dot_product = np.dot(DB, PN)
assert abs(dot_product) < 1e-10, f'수직 조건 실패: {dot_product}'

# 법선벡터
DP = P - D
DC = C - D
n1 = np.cross(DP, DB)
n2 = np.cross(DC, DB)

# 각도 계산
cos_theta = abs(np.dot(n1, n2)) / (np.linalg.norm(n1) * np.linalg.norm(n2))
cos2_theta = cos_theta ** 2
answer = 40 * cos2_theta

if abs(answer - 25) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {answer}')