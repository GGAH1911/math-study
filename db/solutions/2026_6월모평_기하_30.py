import numpy as np
from scipy.optimize import minimize

# A, E 좌표
A = np.array([0, 0])
E = np.array([9, 12])

# 목적함수: AE · AQ를 최소화
def objective(params):
    t, theta = params
    # Q의 좌표: P = (6, t)이고, Q는 중심 (9, t), 반지름 3인 원 위
    Q = np.array([9 + 3*np.cos(theta), t + 3*np.sin(theta)])
    AE = E - A
    AQ = Q - A
    return np.dot(AE, AQ)

# 제약: t는 [0, 8]
result = minimize(objective, x0=[0, np.pi], bounds=[(0, 8), (0, 2*np.pi)])
min_value = result.fun

print('VERIFY_PASS' if abs(min_value - 36) < 1e-6 else f'VERIFY_FAIL: {min_value}')