import numpy as np
A = np.array([[4, 3], [3, 4]])
B = np.array([[8, 2], [2, 8]])
p, q = 2, 4
J = np.array([[0, 1], [1, 0]])
lhs = p * A - B
rhs = q * J
if np.allclose(lhs, rhs):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')