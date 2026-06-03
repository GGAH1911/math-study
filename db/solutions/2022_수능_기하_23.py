import math
A = (2, 1, 3)
P = (2, 1, -3)
Q = (-2, 1, 3)
dist_PQ = math.sqrt((P[0]-Q[0])**2 + (P[1]-Q[1])**2 + (P[2]-Q[2])**2)
expected = 2 * math.sqrt(13)
if abs(dist_PQ - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')