import numpy as np
from scipy.optimize import fsolve

# 주어진 함수 f(x) = x(x^2 - 8x + 19)
def f(x):
    return x * (x**2 - 8*x + 19)

# 함수 g(x) = cbrt(x * f(x)^2)
def g(x):
    return np.cbrt(x * f(x)**2)

# g의 도함수 g'(x)
def g_prime(x):
    if abs(x**2 - 8*x + 19) < 1e-10:
        return float('nan')
    numerator = 7*x**2 - 40*x + 57
    denominator = 3 * np.cbrt(x**2 - 8*x + 19)
    return numerator / denominator

# 극값 조건 확인
val1 = g_prime(19/7)
val2 = g_prime(3)

# f(5) 계산
f_5 = f(5)

# 검증
if abs(val1) < 1e-10 and abs(val2) < 1e-10 and abs(f_5 - 20) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')