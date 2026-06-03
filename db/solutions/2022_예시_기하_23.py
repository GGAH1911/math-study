import numpy as np
P = np.array([1, 3, 4])
Q = np.array([1, -3, 4])
distance = np.linalg.norm(P - Q)
print('VERIFY_PASS' if abs(distance - 6.0) < 1e-9 else 'VERIFY_FAIL')