import math
A = (4, 3, -9)
B = (4, 3, 9)
C = (-4, -3, 9)
dist = math.sqrt((B[0]-C[0])**2 + (B[1]-C[1])**2 + (B[2]-C[2])**2)
if abs(dist - 10) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')