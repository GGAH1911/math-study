import numpy as np

O1 = np.array([8, 2])
O2 = np.array([3, -4])
r1, r2 = 2, 2

p_x = 16/5
q_x = 16/17
P = np.array([p_x, 0])
Q = np.array([q_x, q_x])

dist_O1_P = np.linalg.norm(P - O1)
dist_O2_Q = np.linalg.norm(Q - O2)

O1_to_P = P - O1
A = O1 + (r1 / dist_O1_P) * O1_to_P

O2_to_Q = Q - O2
B = O2 + (r2 / dist_O2_Q) * O2_to_Q

AP = np.linalg.norm(P - A)
PQ = np.linalg.norm(Q - P)
QB = np.linalg.norm(B - Q)

total = AP + PQ + QB
err_A = abs(np.linalg.norm(A - O1) - r1)
err_B = abs(np.linalg.norm(B - O2) - r2)
err_Q = abs(Q[0] - Q[1])

if abs(total - 9) < 1e-9 and err_A < 1e-9 and err_B < 1e-9 and err_Q < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')