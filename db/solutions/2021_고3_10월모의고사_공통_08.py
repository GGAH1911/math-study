import numpy as np
k = 4
alpha = (k - np.sqrt(k**2 - 4)) / 2
beta = (k + np.sqrt(k**2 - 4)) / 2
x1 = alpha
x3 = beta

y1_left = abs(np.log2(-x1 + k))
y1_right = abs(np.log2(x1))
assert abs(y1_left - y1_right) < 1e-10

y3_left = abs(np.log2(-x3 + k))
y3_right = abs(np.log2(x3))
assert abs(y3_left - y3_right) < 1e-10

assert abs((x3 - x1) - 2*np.sqrt(3)) < 1e-10
assert abs((x1 + x3) - 4) < 1e-10

print('VERIFY_PASS')