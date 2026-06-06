import numpy as np

# 주어진 조건
A_plus_B = np.array([[4, 2], [-1, 4]])
A_minus_2B = np.array([[1, 2], [8, -11]])

# 구한 답: B의 성분의 합이 3
# B를 직접 계산: (A+B) - (A-2B) = 3B
three_B = A_plus_B - A_minus_2B
B = three_B / 3

# B의 모든 성분의 합
sum_of_B = np.sum(B)

# 검증: A 계산
A = A_plus_B - B

# 원래 조건 확인
check1 = np.allclose(A + B, A_plus_B)
check2 = np.allclose(A - 2*B, A_minus_2B)

if check1 and check2 and abs(sum_of_B - 3) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')