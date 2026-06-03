import math
A = (1, 3)
B = (2, 7)
distance = math.sqrt((B[0] - A[0])**2 + (B[1] - A[1])**2)
expected = math.sqrt(17)
if abs(distance - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')