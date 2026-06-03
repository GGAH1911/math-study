import numpy as np
m = 1
a = np.array([2*m - 1, 3*m + 1])
b = np.array([3, 12])
det = a[0] * b[1] - a[1] * b[0]
if abs(det) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')