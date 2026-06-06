import math
from scipy.optimize import fsolve

a = 6
f_a = a * (2**a) / (2**a - 1)

# 점 A, B, C 좌표
A = (f_a, math.log2(f_a - a))
B = (f_a, math.log2(f_a))
C = (f_a + a, math.log2(f_a))

# AB = BC 확인
AB = B[1] - A[1]
BC = C[0] - B[0]

if abs(AB - BC) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')