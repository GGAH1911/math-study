import numpy as np
from math import sqrt

v1 = np.array([1, 5])
v2 = np.array([3, 2])

dot_product = np.dot(v1, v2)
mag_v1 = np.linalg.norm(v1)
mag_v2 = np.linalg.norm(v2)

cos_theta = abs(dot_product) / (mag_v1 * mag_v2)
expected = sqrt(2) / 2

if abs(cos_theta - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')