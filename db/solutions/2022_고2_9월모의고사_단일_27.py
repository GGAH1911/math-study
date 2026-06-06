import numpy as np
from scipy.optimize import fminbound

a = 6

def g(x):
    return (x - 1) * (x - 3)

def h(x):
    return (0.5) ** (g(x) - a)

# 구간 [0, 5]에서 최솟값과 최댓값 확인
x_vals = np.linspace(0, 5, 1000)
h_vals = [h(x) for x in x_vals]

min_h = min(h_vals)
max_h = max(h_vals)

print(f'최솟값: {min_h}')
print(f'최댓값: {max_h}')
print(f'최솟값이 1/4 = {1/4}와 일치: {np.isclose(min_h, 0.25)}')
print(f'최댓값이 128과 일치: {np.isclose(max_h, 128)}')

if np.isclose(min_h, 0.25) and np.isclose(max_h, 128):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')