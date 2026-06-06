import numpy as np
from scipy.optimize import fsolve
import sympy as sp

# 정확한 값들
sqrt14 = np.sqrt(14)
sqrt2 = np.sqrt(2)
sqrt7 = np.sqrt(7)

# 좌표
A = np.array([0, 0, sqrt14])
B = np.array([1, -1, 0])
C = np.array([1, 1, 0])
D = np.array([-1, 1, 0])
E = np.array([-1, -1, 0])
P = np.array([1, 0, 0])
Q = np.array([0, 1, 0])
R = np.array([7/8, 7/8, sqrt14/8])

# 구의 중심과 반지름
O = np.array([1/2, 1/2, 0])
r = np.sqrt(2)/2

# 검증: C, P, Q, R이 구 위에 있는가?
dist_C = np.linalg.norm(C - O)
dist_P = np.linalg.norm(P - O)
dist_Q = np.linalg.norm(Q - O)
dist_R = np.linalg.norm(R - O)

assert abs(dist_C - r) < 1e-10
assert abs(dist_P - r) < 1e-10
assert abs(dist_Q - r) < 1e-10
assert abs(dist_R - r) < 1e-10

# S 계산
t0 = 7/8
T = np.array([t0, -t0, sqrt14*(1-t0)])
OT = T - O
OT_norm = np.linalg.norm(OT)
u = OT / OT_norm
S = O + r * u

# S가 구 위에 있는가?
dist_S = np.linalg.norm(S - O)
assert abs(dist_S - r) < 1e-10

# 정사영 넓이 계산
A_prime = np.array([0, 0, 0])
B_prime = np.array([1, -1, 0])
S_prime = np.array([S[0], S[1], 0])

AB = B_prime - A_prime
AS = S_prime - A_prime
cross = np.cross(AB, AS)
area = 0.5 * abs(cross[2])

# 검증: area = 1/2 - √2/6
expected_area = 1/2 - sqrt2/6
assert abs(area - expected_area) < 1e-10

# p + q 계산
p = 1/2
q = -1/6
result = 60 * (p + q)
assert abs(result - 20) < 1e-10

print('VERIFY_PASS')