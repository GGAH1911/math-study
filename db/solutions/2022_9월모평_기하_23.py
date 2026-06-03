import numpy as np
A = np.array([3, 0, -2])
B = np.array([3, 0, 2])
C = np.array([0, 4, 2])
BC_distance = np.linalg.norm(C - B)
if abs(BC_distance - 5.0) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')