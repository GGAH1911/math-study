import numpy as np
from scipy.optimize import fsolve

# c = 4, k = 11
c, k = 4, 11

# Point P
x_P = 2*c - k  # = -3
y_P = np.sqrt(3*c**2 + 2*c*k - k**2)  # sqrt(15)

F = np.array([c, 0])
F_prime = np.array([-c, 0])
P = np.array([x_P, y_P])
Q = np.array([-k, y_P])

# Check ellipse equation: x^2/36 + y^2/(36-c^2) = 1
ellipse_check = (x_P**2 / 36) + (y_P**2 / (36 - c**2))

# Check parabola: y^2 = 2(c+k)x + k^2 - c^2
parabola_lhs = y_P**2
parabola_rhs = 2*(c+k)*x_P + k**2 - c**2

# Check focal property of ellipse
dist_FP = np.linalg.norm(P - F)
dist_FprimeP = np.linalg.norm(P - F_prime)
focal_sum = dist_FP + dist_FprimeP

# Check condition (가): cos(angle F'FP) = 7/8
v1 = F_prime - F
v2 = P - F
cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# Check condition (나): FP - F'Q = PQ - FF'
dist_FQ_prime = np.linalg.norm(Q - F_prime)
dist_PQ = np.linalg.norm(Q - P)
dist_FF_prime = np.linalg.norm(F - F_prime)
cond_b_lhs = dist_FP - dist_FQ_prime
cond_b_rhs = dist_PQ - dist_FF_prime

if (abs(ellipse_check - 1) < 1e-10 and 
    abs(parabola_lhs - parabola_rhs) < 1e-10 and
    abs(focal_sum - 12) < 1e-10 and
    abs(cos_angle - 7/8) < 1e-10 and
    abs(cond_b_lhs - cond_b_rhs) < 1e-10):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')