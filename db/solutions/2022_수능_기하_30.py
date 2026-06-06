import numpy as np
from scipy.optimize import minimize

# 구의 정의
C = np.array([2, np.sqrt(5), 5])
P = np.array([0, 0, 1])
O = np.array([0, 0, 0])

# 평면 OPC 내의 기저
u1 = np.array([2, np.sqrt(5), 0]) / 3
u2 = np.array([0, 0, 1])

# Q: 평면과 구의 교선
def get_Q(theta):
    return C + 5 * np.cos(theta) * u1 + 5 * np.sin(theta) * u2

def get_Q1(theta):
    return get_Q(theta)[:2]

# R: 구 위의 점
def get_R(phi, psi):
    return C + 5 * np.array([np.sin(phi)*np.cos(psi), np.sin(phi)*np.sin(psi), np.cos(phi)])

def get_R1(phi, psi):
    return get_R(phi, psi)[:2]

# 삼각형 넓이
def triangle_area(theta, phi, psi):
    Q1, R1 = get_Q1(theta), get_R1(phi, psi)
    return abs(Q1[0]*R1[1] - Q1[1]*R1[0]) / 2

# 최적화
result = minimize(lambda x: -triangle_area(x[0], x[1], x[2]), [0, 1.5, 0], method='Powell')
theta_opt, phi_opt, psi_opt = result.x
max_area = -result.fun

Q = get_Q(theta_opt)
R = get_R(phi_opt, psi_opt)
PQ, PR = Q - P, R - P
n_PQR = np.cross(PQ, PR) / np.linalg.norm(np.cross(PQ, PR))
n_xy = np.array([0, 0, 1])
cos_angle = abs(np.dot(n_PQR, n_xy))
proj_area = max_area * cos_angle

ratio_value = proj_area / np.sqrt(6)
if abs(ratio_value - 20/3) < 0.01:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')