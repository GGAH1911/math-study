import numpy as np
from scipy.optimize import fminbound

k = 6
alpha = 6
beta = 11

def f(x, k):
    return np.abs(2*np.sin(np.pi*x/k) + 0.5)

# 검증 1: [alpha, alpha+1]에서 최댓값이 0.5인지 확인
x_vals_1 = np.linspace(alpha, alpha+1, 1000)
max_1 = np.max(f(x_vals_1, k))
print(f'[{alpha}, {alpha+1}] 최댓값: {max_1:.6f}')

# 검증 2: [beta, beta+1]에서 최댓값이 0.5인지 확인
x_vals_2 = np.linspace(beta, beta+1, 1000)
max_2 = np.max(f(x_vals_2, k))
print(f'[{beta}, {beta+1}] 최댓값: {max_2:.6f}')

# 검증 3: 경계값 확인
print(f'f({alpha}) = {f(alpha, k):.6f}')
print(f'f({alpha+1}) = {f(alpha+1, k):.6f}')
print(f'f({beta}) = {f(beta, k):.6f}')
print(f'f({beta+1}) = {f(beta+1, k):.6f}')

if abs(max_1 - 0.5) < 1e-10 and abs(max_2 - 0.5) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')