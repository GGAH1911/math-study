import numpy as np
from scipy.optimize import fminbound

# a = 2π/3, b = 5π/6
a = 2*np.pi/3
b = 5*np.pi/6

# 함수 f(x) = 2cos(3x+b)
def f(x):
    return 2*np.cos(3*x + b)

# 구간 [π/2, a]에서의 최댓값과 최솟값
x_vals = np.linspace(np.pi/2, a, 1000)
y_vals = f(x_vals)

max_val = np.max(y_vals)
min_val = np.min(y_vals)

# 검증
tolerance = 1e-10
max_check = abs(max_val - 1.0) < tolerance
min_check = abs(min_val - (-np.sqrt(3))) < tolerance

if max_check and min_check:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: max={max_val}, expected=1.0; min={min_val}, expected={-np.sqrt(3)}')