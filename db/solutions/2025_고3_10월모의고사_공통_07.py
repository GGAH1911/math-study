import numpy as np
from numpy.polynomial import polynomial as P

def f(x):
    return x**3 - 6*x + 7

def f_prime(x):
    return 3*x**2 - 6

# 점 (1, 2)에서의 기울기
m = f_prime(1.0)

# 접선 방정식: y - 2 = m(x - 1)
# y = m*x - m + 2
y_intercept = -m + 2

# 답이 5인지 확인
if abs(y_intercept - 5.0) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')