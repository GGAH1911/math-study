import numpy as np

t = np.pi / 4

# 원래 함수
# x = t + cos(2t), y = sin^2(t)

dx_dt = 1 - 2 * np.sin(2 * t)
dy_dt = np.sin(2 * t)  # = 2*sin(t)*cos(t)

dy_dx = dy_dt / dx_dt

expected = -1

if abs(dy_dx - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL', dy_dx)
