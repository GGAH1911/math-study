import numpy as np

A = np.array([0., 0.])
B = np.array([-1., np.sqrt(3)])
C = np.array([3., np.sqrt(3)])
D = np.array([2., 0.])
P = np.array([-3/2, 3*np.sqrt(3)/2])
Q = np.array([0., 2*np.sqrt(3)])

AC_vec = C - A
AD_vec = D - A
BP_vec = P - B
PQ_vec = Q - P
CP_vec = P - C
DQ_vec = Q - D

ac_inner_pq = np.dot(AC_vec, PQ_vec)
result = np.dot(CP_vec, DQ_vec)

print(f'Condition (나) check: AC·PQ = {ac_inner_pq}')
print(f'CP·DQ = {result}')

QA = A - Q
QB = B - Q
cos_bqa = np.dot(QA, QB) / (np.linalg.norm(QA) * np.linalg.norm(QB))
angle_bqa = np.arccos(cos_bqa)

BP = P - B
BQ = Q - B
cos_pbq = np.dot(BP, BQ) / (np.linalg.norm(BP) * np.linalg.norm(BQ))
angle_pbq = np.arccos(cos_pbq)

if abs(2*angle_bqa - angle_pbq) < 1e-10 and angle_pbq < np.pi/2 and abs(result - 12) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')