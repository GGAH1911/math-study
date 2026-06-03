import numpy as np

p = 0.5
a_sq = 27/4
a = np.sqrt(a_sq)

F1 = np.array([p, a])
F2 = np.array([-1.0, 0.0])

# Check F1F2 = 3
dist_F1F2 = np.linalg.norm(F1 - F2)

# Parametrize line: X(t) = F2 + t*(F1-F2)
dx = F1[0] - F2[0]  # = p+1 = 1.5
dy = F1[1] - F2[1]  # = a

# Q on y^2 = -4x: (F2y + t*dy)^2 = -4*(F2x + t*dx)
# dy^2*t^2 + (2*F2y*dy + 4*dx)*t + (F2y^2 + 4*F2x) = 0
A1 = dy**2
B1 = 2*F2[1]*dy + 4*dx
C1 = F2[1]**2 + 4*F2[0]
disc1 = B1**2 - 4*A1*C1
t_Q_cands = [(-B1 + np.sqrt(disc1))/(2*A1), (-B1 - np.sqrt(disc1))/(2*A1)]
t_Q = [t for t in t_Q_cands if 0 < t < 1][0]

# P on (y-a)^2 = 4px: (F2y + t*dy - a)^2 = 4p*(F2x + t*dx)
u0 = F2[1] - a
A2 = dy**2
B2 = 2*u0*dy - 4*p*dx
C2 = u0**2 - 4*p*F2[0]
disc2 = B2**2 - 4*A2*C2
t_P_cands = [(-B2 + np.sqrt(disc2))/(2*A2), (-B2 - np.sqrt(disc2))/(2*A2)]
t_P = [t for t in t_P_cands if 0 < t < 1][0]

Q_pt = F2 + t_Q*(F1-F2)
P_pt = F2 + t_P*(F1-F2)

check_F1F2 = abs(dist_F1F2 - 3) < 1e-8
check_Q = abs(Q_pt[1]**2 - (-4*Q_pt[0])) < 1e-8
check_P = abs((P_pt[1]-a)**2 - 4*p*P_pt[0]) < 1e-8
check_PQ = abs(np.linalg.norm(P_pt - Q_pt) - 1) < 1e-8
check_ans = abs(a_sq + p**2 - 7) < 1e-8

if all([check_F1F2, check_Q, check_P, check_PQ, check_ans]):
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: F1F2={dist_F1F2:.6f}, Q_ok={check_Q}, P_ok={check_P}, PQ={np.linalg.norm(P_pt-Q_pt):.6f}, ans={a_sq+p**2:.6f}')
