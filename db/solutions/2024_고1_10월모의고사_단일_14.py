import numpy as np
from sympy import *

# 각 a값에 대해 검증
def verify_intersection(a_val):
    # a값에 대해 부등식 범위 계산
    left1, right1 = -9, a_val**2 - 6*a_val
    left2, right2 = 2*a_val - 16, 2*a_val
    
    # 교집합 구하기
    inter_left = max(left1, left2)
    inter_right = min(right1, right2)
    
    if inter_left > inter_right:
        return 0  # 공집합
    elif inter_left == inter_right:
        return 1  # 정확히 한 점
    else:
        return 2  # 구간

results = []
for a in [-4.5, 3, 4]:
    count = verify_intersection(a)
    results.append((a, count))

all_satisfy = all(count == 1 for _, count in results)
if all_satisfy:
    total_sum = sum(a for a, _ in results)
    expected = 5/2
    if abs(total_sum - expected) < 1e-9:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')