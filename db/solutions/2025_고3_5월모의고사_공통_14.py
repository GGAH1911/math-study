import numpy as np

C = np.array([0.0, 0.0])
A = np.array([3.0, 0.0])
D = np.array([8.0, 0.0])
CE_val = 6.0 * np.sqrt(2.0)

# DE=4 조건으로 E 결정 (E = D + 4(cos_a, sin_a)), CE=6√2 사용
cos_a = (CE_val**2 - 80.0) / 64.0
assert -1.0 <= cos_a <= 1.0
sin_a = np.sqrt(1.0 - cos_a**2)
E = np.array([8.0 + 4.0*cos_a, 4.0*sin_a])

# 주어진 길이 검증
assert abs(np.linalg.norm(A - C) - 3.0) < 1e-9
assert abs(np.linalg.norm(D - A) - 5.0) < 1e-9
assert abs(np.linalg.norm(E - D) - 4.0) < 1e-9
assert abs(np.linalg.norm(E - C) - CE_val) < 1e-9

def circumcircle(P1, P2, P3):
    ax, ay = P1; bx, by = P2; cx, cy = P3
    d = 2*(ax*(by-cy) + bx*(cy-ay) + cx*(ay-by))
    ux = ((ax**2+ay**2)*(by-cy) + (bx**2+by**2)*(cy-ay) + (cx**2+cy**2)*(ay-by))/d
    uy = ((ax**2+ay**2)*(cx-bx) + (bx**2+by**2)*(ax-cx) + (cx**2+cy**2)*(bx-ax))/d
    center = np.array([ux, uy])
    return center, np.linalg.norm(P1 - center)

# C_2 = A,D,E 외접원
O2, r2 = circumcircle(A, D, E)

# B는 직선 CE 와 C_2 의 또다른 교점
EE = float(np.dot(E, E)); EO = float(np.dot(E, O2)); OO = float(np.dot(O2, O2))
A_q, B_q, C_q = EE, -2*EO, OO - r2**2
disc = B_q**2 - 4*A_q*C_q
assert disc > 0
t1 = (-B_q + np.sqrt(disc)) / (2*A_q)
t2 = (-B_q - np.sqrt(disc)) / (2*A_q)
t_B = t1 if abs(t1 - 1.0) > abs(t2 - 1.0) else t2
B = t_B * E
assert abs(np.linalg.norm(B - O2) - r2) < 1e-7

# C_1 = C,A,B 외접원
O1, r1 = circumcircle(C, A, B)

ratio = r2 / r1
if abs(ratio - 2.0) < 1e-6:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL ratio={ratio}')
