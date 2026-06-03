import numpy as np
from sympy import symbols, solve

# d=2 검증
d = 2
A = {-4-d, -4, -4+d, -4+2*d, -4+3*d}
B = {-8-d, -8+d, -8+3*d, -8+5*d, -8+7*d}
intersection = A & B
if len(intersection) == 3:
    a20_d2 = -4 + 18*d
else:
    print('VERIFY_FAIL')
    exit()

# d=1 검증
d = 1
A = {-4-d, -4, -4+d, -4+2*d, -4+3*d}
B = {-8-d, -8+d, -8+3*d, -8+5*d, -8+7*d}
intersection = A & B
if len(intersection) == 3:
    a20_d1 = -4 + 18*d
else:
    print('VERIFY_FAIL')
    exit()

# 합 검증
result_sum = a20_d2 + a20_d1
if result_sum == 46:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')