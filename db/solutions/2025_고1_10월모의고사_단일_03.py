import numpy as np

# 원래 행렬
A = np.array([[2, 0], [3, -1]])
B = np.array([[1, 2], [0, 2]])

# A + 2B 계산
result = A + 2*B

# 모든 성분의 합
sum_all = np.sum(result)

if sum_all == 14:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')