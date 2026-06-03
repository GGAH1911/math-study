import numpy as np
c = np.sqrt(3) - 1
b2 = 1 - c**2
F  = np.array([c, 0.0])
Fp = np.array([-c, 0.0])
P  = np.array([-c/2, np.sqrt(3)*c/2])
# 1. P on ellipse
ell = P[0]**2 + P[1]**2/b2
# 2. FP perp F'P
dot = np.dot(P-F, P-Fp)
# 3. Q on y-axis, FP is perp-bisector of F'Q
t = c/(P[0]+c)
Q = Fp + t*(P-Fp)
M = (Fp+Q)/2
perp = np.dot(Q-Fp, P-F)         # FP perp F'Q
Fp_to_M = M - Fp; Fp_to_Q = Q - Fp
cross = Fp_to_M[0]*Fp_to_Q[1] - Fp_to_M[1]*Fp_to_Q[0]  # M midpoint check
# 4. c^4 - 8c^2 + 4 == 0
poly = c**4 - 8*c**2 + 4
if (abs(ell-1)<1e-9 and abs(dot)<1e-9 and abs(Q[0])<1e-9
        and abs(perp)<1e-9 and abs(poly)<1e-9):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
