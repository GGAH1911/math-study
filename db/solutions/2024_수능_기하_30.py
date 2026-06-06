import numpy as np
from scipy.optimize import fminbound

# 정삼각형 ABC 좌표
A = np.array([0, 0])
B = np.array([4, 0])
C = np.array([2, 2*np.sqrt(3)])

# D, E, F
D = A + (1/4)*(B - A)
E = B + (1/4)*(C - B)
F = C + (1/4)*(A - C)

def compute_AX_magnitude_squared(theta):
    P = D + np.array([np.cos(theta), np.sin(theta)])
    Q = E + np.array([np.cos(theta), np.sin(theta)])
    R = F + np.array([np.cos(theta), np.sin(theta)])
    
    PB = B - P
    QC = C - Q
    RA = A - R
    AX = PB + QC + RA
    return np.dot(AX, AX)

# 최대값 확인
theta_opt = 0
max_mag_sq = compute_AX_magnitude_squared(0)

for t in np.linspace(0, 2*np.pi, 100):
    mag_sq = compute_AX_magnitude_squared(t)
    if mag_sq > max_mag_sq:
        max_mag_sq = mag_sq
        theta_opt = t

# 최대값일 때의 P, Q, R
P = D + np.array([np.cos(theta_opt), np.sin(theta_opt)])
Q = E + np.array([np.cos(theta_opt), np.sin(theta_opt)])
R = F + np.array([np.cos(theta_opt), np.sin(theta_opt)])

# 삼각형 PQR의 넓이
PQ = Q - P
PR = R - P
cross_product = PQ[0]*PR[1] - PQ[1]*PR[0]
S = abs(cross_product) / 2

# 16S^2 계산
result = 16 * S**2

if abs(result - 147) < 0.001:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')