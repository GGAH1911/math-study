import numpy as np
from numpy import sqrt, cos, pi

# 설정된 좌표
C = np.array([0, 0])
B = np.array([17*sqrt(3), 0])
A = np.array([0, 17])
D = np.array([5*sqrt(3), 0])
E = np.array([0, 15])

# 조건 검증
BD_length = np.linalg.norm(B - D)
CE_length = np.linalg.norm(E - C)

# 각 CDE 검증
DC = C - D
DE = E - D
cos_CDE = np.dot(DC, DE) / (np.linalg.norm(DC) * np.linalg.norm(DE))
angle_CDE_deg = np.arccos(cos_CDE) * 180 / pi

# 삼각형 ABC 각도 검증
BA = A - B
BC = C - B
cos_ABC = np.dot(BA, BC) / (np.linalg.norm(BA) * np.linalg.norm(BC))
angle_ABC_deg = np.arccos(cos_ABC) * 180 / pi

angle_ACB_deg = 90

# AE 계산
AE_length = np.linalg.norm(E - A)

# 모든 조건 확인
if abs(BD_length - 12*sqrt(3)) < 1e-9 and \
   abs(CE_length - 15) < 1e-9 and \
   abs(angle_CDE_deg - 60) < 1e-9 and \
   abs(angle_ABC_deg - 30) < 1e-9 and \
   abs(AE_length - 2) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')