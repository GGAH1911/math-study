import numpy as np

# A=(0,0), B=(4,0), D=(0,6) => Area(ABD) = (1/2)*4*6 = 12
A = np.array([0.0, 0.0])
B = np.array([4.0, 0.0])
D = np.array([0.0, 6.0])

# From analysis: k = 2/3
k = 2.0 / 3.0
C = B + k * (D - A)  # = (4, 4)

# Verify (가): AD || BC
vec_AD = D - A
vec_BC = C - B
cross_AD_BC = vec_AD[0]*vec_BC[1] - vec_AD[1]*vec_BC[0]
assert abs(cross_AD_BC) < 1e-10, f'(가) 실패: cross={cross_AD_BC}'

# Verify (나): exists t s.t. t*AC = 3*AB + 2*AD
vec_AC = C - A
vec_AB = B - A
rhs = 3*vec_AB + 2*vec_AD
t_val = rhs[0] / vec_AC[0]
assert np.allclose(t_val * vec_AC, rhs), f'(나) 실패'
assert abs(t_val - 3.0) < 1e-9, f't={t_val}, expected 3'

# Verify Area(ABD) = 12
area_ABD = 0.5 * abs(np.cross(B-A, D-A))
assert abs(area_ABD - 12) < 1e-10, f'Area(ABD)={area_ABD}'

# Compute Area(ABCD) shoelace
pts = [A, B, C, D]
n = len(pts)
s = 0.0
for i in range(n):
    j = (i+1) % n
    s += pts[i][0]*pts[j][1] - pts[j][0]*pts[i][1]
area_ABCD = abs(s) / 2.0

if abs(area_ABCD - 20) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: Area(ABCD)={area_ABCD}')