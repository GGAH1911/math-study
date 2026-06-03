import numpy as np

# 주어진 벡터
a = np.array([-6, 0])
b_k = 3  # 우리가 구한 k 값
b = np.array([b_k, 2])

# 조건 검증
result = a + 2 * b
expected = np.array([0, 4])

if np.allclose(result, expected):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')