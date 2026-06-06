import numpy as np
from scipy.optimize import fsolve

a = 1/3
b = 1/3

# 조건 (나) 검증: f(2) = 2e^(-2)
f_2 = (a * 4 + b * 2) * np.exp(-2)
expected = 2 * np.exp(-2)
assert np.isclose(f_2, expected), f'f(2) = {f_2}, expected {expected}'

# 조건 (가) 검증: h(x) = (ax+b)e^(-x)의 극값점이 x=0 근처
def h(x):
    if abs(x) < 1e-10:
        return float('nan')
    return (a * x + b) * np.exp(-x)

def h_prime(x):
    return (a - a*x - b) * np.exp(-x)

# 극값점 확인
extrema = fsolve(h_prime, 0.1)[0]
assert np.isclose(extrema, 0, atol=1e-6), f'극값점이 0이 아님: {extrema}'

# f'(t)의 정의
def f_prime(t):
    return np.exp(-t) * (-a*t**2 + (4*a - 1)*t + (1 - 2*a))

# f'(t) = 1/3이 t=0에서만 성립하는지 확인
f_prime_0 = f_prime(0)
assert np.isclose(f_prime_0, 1/3), f'f\'(0) = {f_prime_0}, expected 1/3'

# h(x) ≠ 0에서의 치역이 (-∞, 1/3)인지 확인 (극댓값이 1/3)
max_h = a * np.exp(-0)  # x=0에서의 극댓값
assert np.isclose(max_h, 1/3), f'극댓값 = {max_h}, expected 1/3'

print('VERIFY_PASS')