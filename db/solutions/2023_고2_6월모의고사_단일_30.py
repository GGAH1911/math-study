import numpy as np
from sympy import *

# a = 2 확인
a = 2
log_a_16 = 4  # log_2(16) = 4

# 세 가지 경우의 k 값
k_values = [-7, 9, 1]

results = []
for k in k_values:
    # f(0) = |0 - k| - 4
    f_0 = abs(0 - k) - 4
    results.append(f_0)
    
    # g(1) 검증: f(1) = |1-k| - 4
    f_1 = abs(1 - k) - 4
    
    if f_1 >= 0:
        g_1 = a ** f_1
    else:
        g_1 = a ** (-f_1)
    
    # 조건 확인: g(1) = 16
    assert abs(g_1 - 16) < 1e-10, f"g(1) != 16 for k={k}"

# 모든 f(a-2) 값의 합
total = sum(results)
assert total == 5, f"Sum is {total}, expected 5"
print('VERIFY_PASS')