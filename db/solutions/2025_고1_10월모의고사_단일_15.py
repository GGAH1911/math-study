import numpy as np
A = np.array([[0, 0], [6, 0]])
B = np.array([[0, 0], [3, 0]])  # b_21 + b_22 = 3 조건, 예시
C = np.array([[2, 0], [2, 0]])
BC = B @ C
if np.allclose(BC, A):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')