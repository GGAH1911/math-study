import numpy as np
from scipy.optimize import fsolve

# 좌표 설정
A = np.array([0, 0, 0])
B = np.array([4, 0, 0])
C = np.array([2, 2*np.sqrt(3), 0])
h = 4 + 2*np.sqrt(3)
D = np.array([0, 0, h])
E = np.array([4, 0, h])
F = np.array([2, 2*np.sqrt(3), h])
G = np.array([0, 0, 2*np.sqrt(3)])

# H의 y 좌표
y_H = 4*np.sqrt(3)/3
H = np.array([4, y_H, 2*np.sqrt(3)])

# 평면 ADFC: y = sqrt(3)*x
# 법벡터 n = (-2*sqrt(3), 2, 0)
n = np.array([-2*np.sqrt(3), 2, 0])
n_norm_sq = np.dot(n, n)

# C와 G는 이미 평면 위에 있는지 확인
assert abs(np.dot(n, C)) < 1e-10, f"C not on plane: {np.dot(n, C)}"
assert abs(np.dot(n, G)) < 1e-10, f"G not on plane: {np.dot(n, G)}"

# H를 평면에 정사영
proj_H = H - (np.dot(n, H) / n_norm_sq) * n

# 정사영 삼각형의 꼭짓점
C_proj = C
G_proj = G
H_proj = proj_H

# 정사영 삼각형의 넓이
v1 = G_proj - C_proj
v2 = H_proj - C_proj
cross = np.cross(v1, v2)
area_sq = np.dot(cross, cross)
S = 0.5 * np.sqrt(area_sq)
S_sq = S * S

if abs(S_sq - 48) < 0.1:
    print("VERIFY_PASS")
else:
    print(f"VERIFY_FAIL: S^2 = {S_sq}, expected 48")