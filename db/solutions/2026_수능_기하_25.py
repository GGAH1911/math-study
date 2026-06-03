import numpy as np
A = np.array([3, -3/2, -2])
B = np.array([-3, -3/2, -2])
C = np.array([-3, 3/2, 2])
dist = np.linalg.norm(C - B)
if abs(dist - 5) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')