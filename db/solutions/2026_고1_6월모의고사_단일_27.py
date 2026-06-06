import numpy as np
from scipy.optimize import fsolve

# 주어진 함수들
def f(x):
    return x**2 - 2*x + 2

def g(x):
    return -x**2 + 8*x - 6

k = 8.2

# f(x) = k의 해 (A, B의 x좌표)
roots_f = np.roots([1, -2, 2-k])
x_A, x_B = sorted(roots_f)
AB_length = x_B - x_A

# g(x) = k의 해 (C, D의 x좌표)
roots_g = np.roots([1, -8, 6+k])
x_C, x_D = sorted(roots_g)
CD_length = x_D - x_C

# AB = 2CD 검증
condition_check = abs(AB_length - 2*CD_length) < 1e-9

# 범위 검증
range_check = 1 < k < 10

# f(x) = k와 g(x) = k 검증
f_check = (abs(f(x_A) - k) < 1e-9) and (abs(f(x_B) - k) < 1e-9)
g_check = (abs(g(x_C) - k) < 1e-9) and (abs(g(x_D) - k) < 1e-9)

if condition_check and range_check and f_check and g_check:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')