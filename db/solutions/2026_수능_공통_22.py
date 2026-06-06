import numpy as np
from scipy.optimize import fsolve
import math

a = 63/4
b = 7/4
c = 7/2
d = 63/2

# 조건 1: b = log_16(8a + 2)
check1 = abs(b - np.log(8*a + 2) / np.log(16))

# 조건 2: d = 4^(c-1) - 1/2
check2 = abs(d - (4**(c-1) - 0.5))

# 조건 3: a + c = 77/4
check3 = abs((a + c) - 77/4)

# 조건 4: b + d = 133/4
check4 = abs((b + d) - 133/4)

# 조건 5: ac = bd
check5 = abs(a*c - b*d)

# 조건 6: 대칭이동 점이 직선 OB 위
check6 = abs(a - 9*b)  # ac = bd에서 d/c = 9

tol = 1e-10
if all([check1 < tol, check2 < tol, check3 < tol, check4 < tol, check5 < tol, check6 < tol]):
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {check1}, {check2}, {check3}, {check4}, {check5}, {check6}')