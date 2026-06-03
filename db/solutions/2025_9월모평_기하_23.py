import numpy as np

# 주어진 벡터
a = np.array([4, 0])
b = np.array([1, 3])

# 조건: 2a + b = (9, k)
result = 2*a + b
k = result[1]

# 검증: 결과가 (9, k) 형태인지 확인
expected_x = 9
expected_y = k

if result[0] == expected_x and result[1] == expected_y:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')