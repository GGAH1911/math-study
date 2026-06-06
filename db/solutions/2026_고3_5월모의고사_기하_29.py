import numpy as np
from scipy.optimize import minimize

# 좌표 설정
D = np.array([1.0, 1.0])
M = np.array([0.5, 1.0])

# 최적점 검증
P = np.array([0.0, 0.0])
Q = np.array([-3/5, -4/5])

# DP와 MQ 벡터
DP = P - D  # (-1, -1)
MQ = Q - M  # (-3/5 - 0.5, -4/5 - 1) = (-11/10, -9/5)

DP_plus_MQ = DP + MQ
magnitude = np.linalg.norm(DP_plus_MQ)

# 예상값
expected = 7/2

if abs(magnitude - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: computed {magnitude}, expected {expected}')