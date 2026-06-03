import numpy as np

A = np.array([8.0, 0.0, 0.0])
B = np.array([0.0, 0.0, 0.0])
C = np.array([0.0, 6.0, 0.0])

# 조건 검증
assert abs(np.linalg.norm(A - B) - 8) < 1e-10, 'AB != 8'
assert abs(np.linalg.norm(B - C) - 6) < 1e-10, 'BC != 6'
assert abs(np.dot(A - B, C - B)) < 1e-10, 'not right angle at B'

# 구 S
M = (A + C) / 2  # (4, 3, 0)
R = np.linalg.norm(A - C) / 2  # 5

# 원 O (y=0 평면과 교원)
d_to_plane = abs(M[1])  # 3
r_O = np.sqrt(R**2 - d_to_plane**2)  # 4
O_center = np.array([M[0], 0.0, M[2]])  # (4, 0, 0)

assert abs(r_O - 4) < 1e-10, 'circle radius != 4'

# P, Q
cos_t = 3.0 / 8.0
sin_t = np.sqrt(1 - cos_t**2)  # sqrt(55)/8
P = O_center + r_O * np.array([cos_t, 0, sin_t])
Q = O_center + r_O * np.array([cos_t, 0, -sin_t])

def dist_to_line(pt, lp, ld):
    v = pt - lp
    return np.linalg.norm(v - np.dot(v, ld) / np.dot(ld, ld) * ld)

line_dir = C - A
dP = dist_to_line(P, A, line_dir)
dQ = dist_to_line(Q, A, line_dir)
PQ = np.linalg.norm(P - Q)

if abs(dP - 4) < 1e-8 and abs(dQ - 4) < 1e-8 and abs(PQ - np.sqrt(55)) < 1e-8:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: dP={dP}, dQ={dQ}, PQ={PQ}, expected={np.sqrt(55)}')
