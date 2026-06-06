import numpy as np
from scipy.optimize import fsolve
import math

# 함수 정의
e = math.e
a = e**2
q = 3*e**2/4
p = 0.5

def f(x):
    return a*(x - p)**2 + q

def g(x):
    return e**x * f(x)

# 검증: g(-6) × g(2) = 129
g_minus6 = g(-6)
g_2 = g(2)
product = g_minus6 * g_2

# 기댓값과 비교
expected_product = 129
error = abs(product - expected_product) / expected_product

if error < 1e-10:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: {product} vs {expected_product}, error={error}')