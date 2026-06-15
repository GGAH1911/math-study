import numpy as np
from scipy import integrate

# Riemann sum 극한값 검증
def f(x):
    return np.sin(3*x)

# 수치적분으로 검증
result, _ = integrate.quad(f, 0, np.pi)
expected = 2/3

# 리만 합으로도 검증 (큰 n으로)
n = 10000
riemann_sum = sum(np.pi/n * f(k*np.pi/n) for k in range(1, n+1))

if abs(result - expected) < 1e-10 and abs(riemann_sum - expected) < 1e-4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')