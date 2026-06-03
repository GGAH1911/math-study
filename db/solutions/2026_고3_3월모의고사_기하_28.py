import numpy as np
sqrt3 = np.sqrt(3)

# Solution parameters
e2 = 3 + 2*sqrt3
a  = 1.0 / (e2 + 3)
b2 = a**2 * (e2 - 1)
fc = a * np.sqrt(e2)
rho = b2 / a

# Points
F_pt  = np.array([fc, 0.0])
Fp_pt = np.array([-fc, 0.0])
P_pt  = np.array([fc, rho])

# 1. P on hyperbola?
p_hyp = P_pt[0]**2/a**2 - P_pt[1]**2/b2

# 2. Find Q: line F'P -> hyperbola
A_c = 4*fc**2/a**2 - rho**2/b2
B_c = -4*fc**2/a**2
C_c = fc**2/a**2 - 1.0
disc = B_c**2 - 4*A_c*C_c
t_r1 = (-B_c + np.sqrt(disc))/(2*A_c)
t_r2 = (-B_c - np.sqrt(disc))/(2*A_c)
t_Q  = t_r2 if abs(t_r1 - 1.0) < 1e-8 else t_r1
Q_pt = np.array([-fc + 2*fc*t_Q, rho*t_Q])

# 3. Q on hyperbola?
q_hyp = Q_pt[0]**2/a**2 - Q_pt[1]**2/b2

# 4. Distances
PQ = np.linalg.norm(P_pt - Q_pt)
FQ = np.linalg.norm(F_pt - Q_pt)

all_pass = (
    abs(p_hyp - 1.0) < 1e-7 and
    abs(q_hyp - 1.0) < 1e-7 and
    0.0 < t_Q < 1.0 and
    abs(PQ - rho) < 1e-7 and
    abs(PQ + FQ - 1.0) < 1e-7 and
    abs(rho - sqrt3/3) < 1e-9
)
print('VERIFY_PASS' if all_pass else 'VERIFY_FAIL')