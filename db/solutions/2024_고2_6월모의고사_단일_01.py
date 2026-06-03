from sympy import *
import math

# 원래 문제 식: 4 × 2^2의 4제곱근
result = (4 * (2**2)) ** (1/4)
print(f'√[4](4 × 2^2) = {result}')

# 정확한 계산
result_exact = nsimplify((4 * (2**2)) ** (1/4))
print(f'정확값: {result_exact}')

# 답 검증: 2^4 = 16
verify = 2 ** 4
print(f'검증: 2^4 = {verify}')
print(f'루트 안의 값: {4 * (2**2)}')

if abs(result - 2.0) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')