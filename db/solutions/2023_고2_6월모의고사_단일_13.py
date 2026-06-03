from sympy import *
import numpy as np

# 부등식을 만족하는 정수 개수 검증
count = 0
valid_integers = []

for x_val in range(-10, 20):
    # 원래 부등식: (2^x - 8)(1/3^x - 9) >= 0
    term1 = 2**x_val - 8
    term2 = 1/(3**x_val) - 9
    product = term1 * term2
    
    if product >= -1e-10:  # 수치오차 고려
        count += 1
        valid_integers.append(x_val)

if count == 6 and valid_integers == [-2, -1, 0, 1, 2, 3]:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: count={count}, integers={valid_integers}')