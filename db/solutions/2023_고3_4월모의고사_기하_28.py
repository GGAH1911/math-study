import numpy as np

sqrt6 = np.sqrt(6)
sqrt7 = np.sqrt(7)

# Parameters
s = sqrt7 - sqrt6
p = (4*sqrt6 - 3*sqrt7) / 3

# Points
P = np.array([p**2, 2*p])
Q = np.array([s**2, 2*s])
F = np.array([1.0, 0.0])
H = np.array([-1.0, 2*p])

# 1. P, Q on parabola y^2 = 4x
assert abs(P[1]**2 - 4*P[0]) < 1e-9, 'P not on parabola'
assert abs(Q[1]**2 - 4*Q[0]) < 1e-9, 'Q not on parabola'

# 2. Q on circle with diameter PF => QP . QF = 0
QP = P - Q
QF = F - Q
assert abs(np.dot(QP, QF)) < 1e-9, 'Q not on circle'

# 3. tan(beta)/tan(alpha) = 3
def angle_tan(v1, v2):
    cross = abs(v1[0]*v2[1] - v1[1]*v2[0])
    dot = abs(np.dot(v1, v2))
    return cross / dot

HP = P - H
HQ = Q - H
PH = H - P
PQ = Q - P

tan_alpha = angle_tan(HP, HQ)  # angle QHP at H
tan_beta  = angle_tan(PH, PQ)  # angle HPQ at P
ratio = tan_beta / tan_alpha
assert abs(ratio - 3) < 1e-9, f'tan_beta/tan_alpha = {ratio:.8f}, not 3'

# 4. QH/PQ = sqrt(105)/7
QH_dist = np.linalg.norm(Q - H)
PQ_dist = np.linalg.norm(P - Q)
result = QH_dist / PQ_dist
expected = np.sqrt(105) / 7

if abs(result - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result:.10f}, expected {expected:.10f}')
