import numpy as np
from scipy.optimize import fminbound

# a = 5일 때 f(x) = -x^2 - 4x + 5
a = 5

# [0,1]에서 g'(x) = f(x) = -x^2 - 4x + a ≥ 0인지 확인
def f(x):
    return -x**2 - 4*x + a

# [0,1]에서 최솟값 구하기
x_test = np.linspace(0, 1, 1000)
f_vals = f(x_test)

min_val = np.min(f_vals)

if min_val >= -1e-10:  # 수치오차 고려
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')