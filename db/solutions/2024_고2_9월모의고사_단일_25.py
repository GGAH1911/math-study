import numpy as np
from math import pi, cos, sin

# 조건을 만족하는 자연수들
candidates = [2, 3, 4, 5, 6]
all_pass = True

for x in candidates:
    cos_val = cos(pi/5 * x)
    sin_val = sin(pi/5 * x)
    satisfies = cos_val < sin_val
    if not satisfies:
        all_pass = False
        break

# 범위 내 다른 자연수들이 조건을 만족하지 않는지 확인
for x in range(1, 11):
    cos_val = cos(pi/5 * x)
    sin_val = sin(pi/5 * x)
    should_satisfy = x in candidates
    does_satisfy = cos_val < sin_val
    if should_satisfy != does_satisfy:
        all_pass = False
        break

if all_pass:
    answer_sum = sum(candidates)
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')