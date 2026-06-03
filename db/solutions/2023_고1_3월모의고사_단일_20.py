import numpy as np

r = np.sqrt(3) + 1

O = np.array([0.0, 0.0])
A = np.array([-r/2, r*np.sqrt(3)/2])
B = np.array([r, 0.0])
C = np.array([0.0, r])
D = np.array([r*np.sqrt(3)/2, r/2])

# Verify angle AOC = 30 deg
ang_OA = np.degrees(np.arctan2(A[1], A[0]))
ang_OC = np.degrees(np.arctan2(C[1], C[0]))
assert abs((ang_OA - ang_OC) - 30.0) < 1e-9, 'AOC angle fail'

# Verify angle DOB = 30 deg
ang_OD = np.degrees(np.arctan2(D[1], D[0]))
assert abs(ang_OD - 30.0) < 1e-9, 'DOB angle fail'

# Find E: OC (x=0) ∩ AD
t = -A[0] / (D[0] - A[0])
E = A + t * (D - A)
assert abs(E[0]) < 1e-9, 'E not on y-axis'

# Find F: perp bisector of OD ∩ OB (y=0)
M = D / 2
perp = np.array([-( D[1]-O[1]), D[0]-O[0]])
s = -M[1] / perp[1]
F = M + s * perp
assert abs(F[1]) < 1e-9, 'F not on OB'

# Verify BF
BF = np.linalg.norm(B - F)
expected_BF = 2*np.sqrt(3)/3
assert abs(BF - expected_BF) < 1e-9, f'BF mismatch: {BF} vs {expected_BF}'

# Area of ODE
v1 = D - O
v2 = E - O
area = 0.5 * abs(v1[0]*v2[1] - v1[1]*v2[0])
expected_area = (3 + np.sqrt(3)) / 2

if abs(area - expected_area) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: area={area}, expected={expected_area}')
