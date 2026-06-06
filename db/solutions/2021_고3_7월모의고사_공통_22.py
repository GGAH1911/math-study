import sympy as sp
import numpy as np
from scipy.optimize import fsolve

# 원래 함수 f(x) 정의
def f(x):
    return (2 * np.sqrt(3) / 3) * x * (x - 3) * (x + 3)

# g(x) 정의
def g(x):
    if -3 <= x < 3:
        return f(x)
    else:
        k = int((x + 3) // 6)
        if 6*k - 3 <= x < 6*k + 3:
            return (1 / (k + 1)) * f(x - 6*k)
    return None

# 각 n에 대해 교점 개수 계산
total = 0
for n in range(1, 13):
    count = 0
    # 각 구간에서 극대값 확인
    for k in range(20):  # 충분히 큰 범위
        max_val = 12 / (k + 1)
        if max_val < n:
            break
        if max_val > n:
            count += 2
        elif max_val == n:
            count += 1
    total += count

if total == 64:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')