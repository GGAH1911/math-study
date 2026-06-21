import numpy as np
from scipy import integrate

def f(x):
    return np.cos(np.pi/2 + x)

def integrand(x):
    return x * np.sin(x)

# 직접 적분 계산
integral_value, _ = integrate.quad(integrand, 0, np.pi)
result = -integral_value / np.pi

print(f'Integral of x*sin(x) from 0 to pi: {integral_value}')
print(f'Result: {result}')
print(f'Expected: -1')
print(f'Match: {np.isclose(result, -1)}')

# 수치적 리만 합 검증
for n in [100, 1000, 10000, 100000]:
    riemann_sum = sum((k * np.pi / n**2) * np.cos(np.pi/2 + k*np.pi/n) for k in range(1, n+1))
    print(f'n={n}: Riemann sum = {riemann_sum:.8f}')

if np.isclose(result, -1):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')