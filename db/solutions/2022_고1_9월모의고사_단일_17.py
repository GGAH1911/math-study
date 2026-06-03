import math
from sympy import sqrt, simplify

# 최적 점들
A = (2, 3)
D = (1, 1)
C = (-1, 0)
B = (-3, 1)

# 거리 계산
AD = math.sqrt((D[0]-A[0])**2 + (D[1]-A[1])**2)
CD = math.sqrt((D[0]-C[0])**2 + (D[1]-C[1])**2)
BC = math.sqrt((C[0]-B[0])**2 + (C[1]-B[1])**2)

total = AD + CD + BC

# 예상값
expected = 3 * math.sqrt(5)

if abs(total - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')