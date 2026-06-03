import numpy as np
A = np.array([[3, 5], [4, 6]])
B = np.array([[1, 2], [2, 4]])
AB = A @ B
result = AB[1, 0]
print('VERIFY_PASS' if result == 16 else 'VERIFY_FAIL')