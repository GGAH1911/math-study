import numpy as np
from sympy import *

# 수렴 조건: -1 < |k/3| - 2 <= 1
# 즉, 1 < |k/3| <= 3
# 즉, 3 < |k| <= 9

count = 0
valid_k = []

for k in range(-20, 21):
    r = abs(k/3) - 2
    # r^n이 수렴하는 조건: -1 < r <= 1
    if -1 < r <= 1:
        count += 1
        valid_k.append(k)

print(f'수렴하는 k 개수: {count}')
print(f'수렴하는 k: {sorted(valid_k)}')

# 검증: k = ±4부터 ±9까지 정확히 12개
expected = [-9, -8, -7, -6, -5, -4, 4, 5, 6, 7, 8, 9]
if sorted(valid_k) == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')