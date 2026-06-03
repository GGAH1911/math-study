import math
A = (5, -5)
B = (1, 7)
OA = math.sqrt(A[0]**2 + A[1]**2)
OB = math.sqrt(B[0]**2 + B[1]**2)
if abs(OA - OB) < 1e-9 and 7 > 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')