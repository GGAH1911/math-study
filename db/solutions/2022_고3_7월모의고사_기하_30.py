import numpy as np
from scipy.optimize import fsolve

# 좌표
O = np.array([0, 0, 0])
A = np.array([4, 0, 0])
P = np.array([2, 0, 2*np.sqrt(3)])
B = np.array([-1, np.sqrt(15), 0])
C = np.array([-1, -np.sqrt(15), 0])

# 구 위에 있는지 확인
P_dist = np.linalg.norm(P)
assert abs(P_dist - 4) < 1e-10, f'P not on sphere: {P_dist}'

# ∠PAO = π/3 확인
AP = P - A
AO = O - A
cos_PAO = np.dot(AP, AO) / (np.linalg.norm(AP) * np.linalg.norm(AO))
assert abs(cos_PAO - 0.5) < 1e-10, f'∠PAO incorrect: {np.arccos(cos_PAO)}'

# cos(∠PAB) = √10/8 확인
AB = B - A
cos_PAB = np.dot(AP, AB) / (np.linalg.norm(AP) * np.linalg.norm(AB))
expected_cos_PAB = np.sqrt(10) / 8
assert abs(cos_PAB - expected_cos_PAB) < 1e-10, f'∠PAB incorrect: {cos_PAB}'

# 정사영 넓이 계산
cross_AP_AB = np.cross(AP, AB)
cross_AP_AC = np.cross(AP, C - A)
area_PAB = 0.5 * np.linalg.norm(cross_AP_AB)

# 두 평면의 법선 벡터 사이의 각
dot_product = np.dot(cross_AP_AB, cross_AP_AC)
mag1 = np.linalg.norm(cross_AP_AB)
mag2 = np.linalg.norm(cross_AP_AC)
cos_theta = abs(dot_product) / (mag1 * mag2)

# 정사영의 넓이
S = area_PAB * cos_theta
S_squared = S * S
result = 30 * S_squared

assert abs(result - 50) < 1e-10, f'Answer incorrect: {result}'
print('VERIFY_PASS')