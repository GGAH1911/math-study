import numpy as np

B = np.array([0.0, 0.0])
C = np.array([4.0, 0.0])
A = np.array([1.0, 1.0])
D = np.array([3.0, 1.0])

# 원래 조건 검증
AD = np.linalg.norm(D - A)
AB = np.linalg.norm(B - A)
CD_len = np.linalg.norm(D - C)

def angle_deg(v1, v2):
    c = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    return np.degrees(np.arccos(np.clip(c, -1, 1)))

angle_ABC = angle_deg(A - B, C - B)
angle_BCD = angle_deg(B - C, D - C)

conds = [
    abs(AD - 2) < 1e-9,
    abs(AB - np.sqrt(2)) < 1e-9,
    abs(CD_len - np.sqrt(2)) < 1e-9,
    abs(angle_ABC - 45) < 1e-9,
    abs(angle_BCD - 45) < 1e-9,
]
assert all(conds), f'조건 불만족: {conds}'

# E: 대각선 AC, BD 교점
M = np.column_stack([C - A, -(D - B)])
params = np.linalg.solve(M, B - A)
t_E = params[0]
E = A + t_E * (C - A)

# H: A에서 BC(x축)에 내린 수선의 발
H = np.array([A[0], 0.0])

# F: AH(x=1 수직선)와 BD 교점
s_F = (A[0] - B[0]) / (D[0] - B[0])
F = B + s_F * (D - B)

AF_vec = F - A
CE_vec = E - C
dot = np.dot(AF_vec, CE_vec)

expected = -4.0 / 9.0
if abs(dot - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {dot:.10f}, expected {expected:.10f}')
