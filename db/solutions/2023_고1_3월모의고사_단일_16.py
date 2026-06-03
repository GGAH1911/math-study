import numpy as np
a = 1
theta = 132 * np.pi / 180

# 마름모 좌표
A = np.array([0, 0])
B = np.array([a, 0])
D = np.array([a*np.cos(theta), a*np.sin(theta)])
C = np.array([a + a*np.cos(theta), a*np.sin(theta)])
E = np.array([a, 2*a*np.sin(theta)])

# ∠ADE 검증
vec_DA = A - D
vec_DE = E - D
cos_ADE = np.dot(vec_DA, vec_DE) / (np.linalg.norm(vec_DA) * np.linalg.norm(vec_DE))
angle_ADE = np.arccos(cos_ADE) * 180 / np.pi

# ∠CEB 검증
vec_EC = C - E
vec_EB = B - E
cos_CEB = np.dot(vec_EC, vec_EB) / (np.linalg.norm(vec_EC) * np.linalg.norm(vec_EB))
angle_CEB = np.arccos(cos_CEB) * 180 / np.pi

# 수직이등분 검증
BE_midpoint = (B + E) / 2
BE_vec = E - B
CD_vec = D - C

if abs(angle_ADE - 72.0) < 0.1 and abs(angle_CEB - 42.0) < 0.1 and abs(BE_midpoint[1] - a*np.sin(theta)) < 1e-10 and abs(np.dot(BE_vec, CD_vec)) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')