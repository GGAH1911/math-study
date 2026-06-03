import math
from math import sqrt

# 좌표 설정
A = (0, 0)
B = (sqrt(2), 0)
C = (0, sqrt(2))
D = (sqrt(2)/3, sqrt(2)/3)
E = (7*sqrt(2)/3, sqrt(2)/3)
F = (sqrt(2)/3, 7*sqrt(2)/3)
P1 = (2*sqrt(2)/3, sqrt(2)/3)
P2 = (sqrt(2)/3, 2*sqrt(2)/3)

# 조건 검증
AB = sqrt((B[0]-A[0])**2 + (B[1]-A[1])**2)
AC = sqrt((C[0]-A[0])**2 + (C[1]-A[1])**2)
DE = sqrt((E[0]-D[0])**2 + (E[1]-D[1])**2)
DF = sqrt((F[0]-D[0])**2 + (F[1]-D[1])**2)
EF = sqrt((F[0]-E[0])**2 + (F[1]-E[1])**2)
BC = sqrt((C[0]-B[0])**2 + (C[1]-B[1])**2)

assert abs(AB - sqrt(2)) < 1e-9
assert abs(AC - sqrt(2)) < 1e-9
assert abs(DE - 2*sqrt(2)) < 1e-9
assert abs(DF - 2*sqrt(2)) < 1e-9
assert abs(EF - 4) < 1e-9

# 둘레 계산
dist_AB = sqrt((B[0]-A[0])**2 + (B[1]-A[1])**2)
dist_BP1 = sqrt((P1[0]-B[0])**2 + (P1[1]-B[1])**2)
dist_P1E = sqrt((E[0]-P1[0])**2 + (E[1]-P1[1])**2)
dist_EF = sqrt((F[0]-E[0])**2 + (F[1]-E[1])**2)
dist_FP2 = sqrt((P2[0]-F[0])**2 + (P2[1]-F[1])**2)
dist_P2C = sqrt((C[0]-P2[0])**2 + (C[1]-P2[1])**2)
dist_CA = sqrt((A[0]-C[0])**2 + (A[1]-C[1])**2)

perimeter = dist_AB + dist_BP1 + dist_P1E + dist_EF + dist_FP2 + dist_P2C + dist_CA
expected = (16 + 16*sqrt(2))/3

if abs(perimeter - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')