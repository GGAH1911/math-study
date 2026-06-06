import numpy as np
from scipy.optimize import minimize_scalar

# 점들의 좌표
sqrt3 = np.sqrt(3)
D = np.array([2*sqrt3, 2])
Q = np.array([3 + 2*sqrt3, 2 + sqrt3])
A = np.array([2 + 2*sqrt3, 0])

# 원의 중심과 반지름
center = np.array([2 + 2*sqrt3, 2])
radius = 2

# DQ 벡터
DQ = Q - D

# 원 위의 점 R에서 DQ·AR의 최댓값을 구함
def objective(theta):
    R = center + radius * np.array([np.cos(theta), np.sin(theta)])
    AR = R - A
    return -np.dot(DQ, AR)  # 최소화하므로 음수

result = minimize_scalar(objective, bounds=(0, 2*np.pi), method='bounded')
max_value = -result.fun
M = max_value
M_squared = M**2

# 검증
if abs(M_squared - 108) < 0.001:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')