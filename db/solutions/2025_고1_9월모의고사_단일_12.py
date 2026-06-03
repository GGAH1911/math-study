import numpy as np
P = np.array([[120, 160], [130, 140]])
Q = np.array([[0.2, 0.8], [0.7, 0.3]])
PQ = P @ Q
result = PQ[1, 1]
if abs(result - 146) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')