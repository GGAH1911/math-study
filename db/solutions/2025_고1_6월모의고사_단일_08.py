import numpy as np
from numpy.polynomial import polynomial as P

# 원래 방정식: x^2 - 3x + 5 = 0
# 근의 공식으로 두 근 구하기
coeffs = [1, -3, 5]  # x^2 - 3x + 5
roots = np.roots(coeffs)
alpha, beta = roots[0], roots[1]

# 원래 식에서 계산
result = alpha**2 * beta + alpha * beta**2 - alpha * beta
result_real = result.real

# 오차 범위 내에서 10인지 확인
if abs(result_real - 10) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')