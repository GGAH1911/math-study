import numpy as np
from scipy.optimize import fsolve

# 타원 확인
P_x = 3 * np.sqrt(3) / 2
P_y = 5 / 2
ellipse_check = (P_x**2) / 9 + (P_y**2) / 25
assert abs(ellipse_check - 1.0) < 1e-10

# 각도 조건 확인
F = np.array([0, 4])
F_prime = np.array([0, -4])
P = np.array([P_x, P_y])

vec_FF_prime = F_prime - F
vec_FP = P - F
cos_angle = np.dot(vec_FF_prime, vec_FP) / (np.linalg.norm(vec_FF_prime) * np.linalg.norm(vec_FP))
assert abs(cos_angle - 0.5) < 1e-10  # cos(pi/3) = 0.5

# 직선 FP와 x축 교점
Q_x = 4 * np.sqrt(3)
Q_y = 0
Q = np.array([Q_x, Q_y])

# 포물선 위의 P 확인
PQ_dist = np.linalg.norm(P - Q)
a = (3 * np.sqrt(3) - 10) / 2
P_directrix_dist = P_x - a
assert abs(PQ_dist - P_directrix_dist) < 1e-10

# R 확인
R_x = 43 * np.sqrt(3) / 2 + 30
R_y = -35/2 - 10 * np.sqrt(3)
R = np.array([R_x, R_y])

# R이 포물선 위에 있는지 확인
RQ_dist = np.linalg.norm(R - Q)
R_directrix_dist = R_x - a
assert abs(RQ_dist - R_directrix_dist) < 1e-10

# R이 직선 FP 위에 있는지 확인
line_check = 4 - (np.sqrt(3)/3) * R_x
assert abs(R_y - line_check) < 1e-10

# PR 계산
PR = np.linalg.norm(R - P)
expected_PR = 40 + 20 * np.sqrt(3)
assert abs(PR - expected_PR) < 1e-10

print('VERIFY_PASS')