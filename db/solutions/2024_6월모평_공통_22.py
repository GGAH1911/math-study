import numpy as np
from scipy.optimize import fsolve

# a = -2 확인
a = -2

# f(x) = x^3 - 2ax^2 = x^3 + 4x^2
# f'(x) = 3x^2 + 8x

def f_prime(x):
    return 3*x**2 + 8*x

# f'(10) 계산
result = f_prime(10)

# 검증
if result == 380:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')