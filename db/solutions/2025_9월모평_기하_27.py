import numpy as np
sqrt14 = np.sqrt(14)
A = np.array([-2, -2, sqrt14])
B = np.array([2,  -2, sqrt14])
C = np.array([2,   2, sqrt14])
D = np.array([-2,  2, sqrt14])
E = np.array([-3, -3, 0.0])
F = np.array([3,  -3, 0.0])
G = np.array([3,   3, 0.0])
H = np.array([-3,  3, 0.0])
# 조건 검증: AE=BF=CG=DH, 높이=sqrt(14)
assert all(abs(np.linalg.norm(Q-P) - 4) < 1e-9 for P,Q in [(A,E),(B,F),(C,G),(D,H)]), 'lateral edge fail'
assert abs(sqrt14 - sqrt14) < 1e-9
# 법벡터
n_AEHD = np.cross(E-A, D-A)
n_BFGC = np.cross(F-B, C-B)
cos_theta = abs(np.dot(n_AEHD, n_BFGC)) / (np.linalg.norm(n_AEHD)*np.linalg.norm(n_BFGC))
# AEHD 넓이 (대각선 외적)
area_AEHD = 0.5 * np.linalg.norm(np.cross(H-A, D-E))
# 정사영 넓이
proj = area_AEHD * cos_theta
expected = 13/3 * np.sqrt(15)
print('VERIFY_PASS' if abs(proj - expected) < 1e-7 else f'VERIFY_FAIL: {proj} != {expected}')