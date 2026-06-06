import numpy as np
from scipy.optimize import fsolve

# 주어진 모든 순서쌍 검증
valid_pairs = [(1,2), (2,4), (3,5), (3,1), (4,1), (5,1), (3,3), (4,3), (5,3)]
a_plus_b_values = []

for a, b in valid_pairs:
    # A: x=pi에서의 점, n(A) = 1
    n_A = 1
    
    # B: sin(x) = (1-b)/a를 만족하는 x ∈ (0, 2π)의 개수
    sin_B = (1 - b) / a
    if -1 < sin_B < 1:
        n_B = 2
    elif sin_B == -1 or sin_B == 1:
        n_B = 1
    else:
        n_B = 0
    
    # C: sin(x) = (3-b)/a를 만족하는 x ∈ (0, 2π)의 개수
    sin_C = (3 - b) / a
    if -1 < sin_C < 1:
        n_C = 2
    elif sin_C == -1 or sin_C == 1:
        n_C = 1
    else:
        n_C = 0
    
    # n(A ∩ B): (π, b) ∈ B인지 확인
    n_A_cap_B = 1 if b == 1 else 0
    
    # n(A ∩ C): (π, b) ∈ C인지 확인
    n_A_cap_C = 1 if b == 3 else 0
    
    # B ∩ C = ∅ (항상)
    n_B_cap_C = 0
    
    # n(A ∪ B ∪ C) = n(A) + n(B) + n(C) - n(A∩B) - n(A∩C) - n(B∩C) + n(A∩B∩C)
    n_A_cap_B_cap_C = 0
    n_union = n_A + n_B + n_C - n_A_cap_B - n_A_cap_C - n_B_cap_C + n_A_cap_B_cap_C
    
    if n_union == 3:
        a_plus_b_values.append(a + b)

M = max(a_plus_b_values)
m = min(a_plus_b_values)
result = M * m

if result == 24:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')