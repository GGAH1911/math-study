import numpy as np
from fractions import Fraction

# Case: d_a = 1, a_1 = -1, d_b = 2, b_1 = -6, m = 6
a = [n - 2 for n in range(1, 7)]
b = [2*n - 8 for n in range(1, 7)]

# 조건 (가) 검증
assert abs(a[0] - b[0]) == 5, f'|a_1 - b_1| = {abs(a[0] - b[0])} != 5'

# 조건 (나) 검증
assert a[5] == b[5], f'a_6={a[5]}, b_6={b[5]}'
a7 = 7 - 2
b7 = 2*7 - 8
assert a7 < b7, f'a_7={a7} not < b_7={b7}'

# 합 조건 검증
assert sum(a) == 9, f'sum(a_k) = {sum(a)} != 9'

# 최종 답
answer_sum = sum(b)
assert answer_sum == -6, f'sum(b_k) = {answer_sum} != -6'
print('VERIFY_PASS')