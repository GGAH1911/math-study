import numpy as np

a = 7
b = 2

def f(x):
    return a * np.cos(b * x) + 1

# 최댓값 확인
x_vals = np.linspace(0, 4 * np.pi, 100000)
max_val = np.max(f(x_vals))
assert abs(max_val - 8) < 1e-6, f'최댓값 오류: {max_val}'

# 주기 확인: f(x + π) == f(x)
x_test = np.array([0.1, 0.5, 1.2, 2.3])
period = np.pi
assert np.allclose(f(x_test + period), f(x_test), atol=1e-9), '주기 오류'

# a, b 양수 확인
assert a > 0 and b > 0, 'a, b 양수 조건 오류'

print('VERIFY_PASS')
