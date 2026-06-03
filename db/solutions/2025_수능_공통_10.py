import numpy as np

a, b = 10, 6

# 1) f(pi/3) = 13 인지 확인
x0 = np.pi / 3
f_x0 = a * np.cos(b * x0) + 3

# 2) [0, 2pi] 전체 최댓값이 13인지 확인
xs = np.linspace(0, 2 * np.pi, 2_000_000)
f_max = np.max(a * np.cos(b * xs) + 3)

# 3) x=pi/3 이 실제 최댓값 달성점인지
if abs(f_x0 - 13) < 1e-8 and abs(f_max - 13) < 1e-5:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: f(pi/3)={f_x0}, max={f_max}')
