import numpy as np
A = np.array([[1, -2], [1, -2]])
B = np.array([[4, 2], [2, 1]])
AB = A @ B
A_plus_2B = A + 2*B
expected_sum = np.array([[9, 2], [5, 0]])
if np.allclose(AB, np.zeros((2,2))) and np.allclose(A_plus_2B, expected_sum):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')