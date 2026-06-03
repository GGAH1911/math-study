import numpy as np

# Answer to verify: semi-major axis a = 7, major axis = 14
a = 7.0
c = 5.0
b_sq = a**2 - c**2  # 24
r = a - c           # 2

F  = np.array([5.0,  0.0])
Fp = np.array([-5.0, 0.0])  # F'
A  = np.array([a, 0.0])

# P on circle C, y > 0
x_P = 5 - r**2 / 10
y_P = r * np.sqrt(100 - r**2) / 10
P = np.array([x_P, y_P])

# Q coordinates
Q = np.array([-5 - 3*r**2/20, 3*r*np.sqrt(100-r**2)/20])

errs = []
# (1) A on ellipse
errs.append(abs(A[0]**2/a**2 + A[1]**2/b_sq - 1))
# (2) P on circle C
errs.append(abs(np.linalg.norm(P - F) - r))
# (3) cond (가): FP ⊥ F'P  (tangent)
errs.append(abs(np.dot(P - F, P - Fp)))
# (4) Q on ellipse
errs.append(abs(Q[0]**2/a**2 + Q[1]**2/b_sq - 1))
# (5) Q in second quadrant
if not (Q[0] < 0 and Q[1] > 0):
    errs.append(1.0)
else:
    errs.append(0.0)
# (6) cond (나): QF' ⊥ PF'
errs.append(abs(np.dot(Q - Fp, P - Fp)))
# (7) QF' = (3/2)PF
errs.append(abs(np.linalg.norm(Q - Fp) - 1.5 * r))
# (8) AF < FF'
if not (np.linalg.norm(A - F) < np.linalg.norm(F - Fp)):
    errs.append(1.0)
else:
    errs.append(0.0)

if all(e < 1e-9 for e in errs):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', errs)
