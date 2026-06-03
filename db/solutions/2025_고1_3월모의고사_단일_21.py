import numpy as np

AB, BC, DG_len, area_DHG_target = 30, 45, 10, 35

# 넓이 DHG = 15q/11 = 35 → q = 77/3
q = 77/3
p = np.sqrt(AB**2 - q**2)

B = np.array([0.0, 0.0])
C = np.array([45.0, 0.0])
A = np.array([p, q])
D = np.array([p + 45.0, q])

# E: C의 이등분선 ∩ line AB
unit_CB = (B - C) / np.linalg.norm(B - C)
unit_CD = (D - C) / np.linalg.norm(D - C)
bisect_dir = unit_CB + unit_CD
t_E = 45*q / (p*bisect_dir[1] - q*bisect_dir[0])
E = C + t_E * bisect_dir
assert abs(q*E[0] - p*E[1]) < 1e-6, 'E not on AB'

# F: line CE ∩ segment BD
CE_dir = E - C
BD_dir = D - B
M = np.column_stack([CE_dir, -BD_dir])
ts = np.linalg.solve(M, B - C)
F = C + ts[0] * CE_dir
assert 0 <= ts[1] <= 1, 'F not on BD'

# G: DG=10 on CD
G = D + DG_len * (C - D) / np.linalg.norm(C - D)
assert abs(np.linalg.norm(G - D) - DG_len) < 1e-6, 'DG length wrong'

# H: line EG ∩ segment BD
EG_dir = G - E
M2 = np.column_stack([EG_dir, -BD_dir])
ts2 = np.linalg.solve(M2, B - E)
H = E + ts2[0] * EG_dir
assert 0 <= ts2[1] <= 1, 'H not on BD'

def tri_area(P1, P2, P3):
    v1, v2 = P2 - P1, P3 - P1
    return 0.5 * abs(v1[0]*v2[1] - v1[1]*v2[0])

a_dhg = tri_area(D, H, G)
a_efh = tri_area(E, F, H)

if abs(a_dhg - 35) < 0.01 and abs(a_efh - 189) < 0.01:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: DHG={a_dhg:.4f}, EFH={a_efh:.4f}')