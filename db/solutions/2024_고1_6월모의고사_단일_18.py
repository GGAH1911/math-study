import numpy as np

a, b = 4, 6

def f(x):
    return x**2 - (2*a - b)*x + a**2 - 4*b

xs = np.linspace(-2, 2, 100001)
ys = f(xs)

min_idx = np.argmin(ys)
max_idx = np.argmax(ys)

min_x = xs[min_idx]
max_y = ys[max_idx]

# 조건(가): 최솟값이 x=1에서
cond_ga = abs(min_x - 1.0) < 0.001
# 조건(나): 최댓값 = 0
cond_na = abs(max_y - 0.0) < 1e-6
# a+b = 10
cond_sum = (a + b == 10)

if cond_ga and cond_na and cond_sum:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: min_x={min_x:.4f}, max_y={max_y:.8f}, a+b={a+b}')
