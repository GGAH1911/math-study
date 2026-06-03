import numpy as np

# 포물선 y^2 = -12(x-1), 준선 x=k=4, 초점 F=(-2, 0)
k = 4
focus = (-2, 0)

# 포물선 위의 임의 점들로 정의 검증 (y값 샘플링)
y_vals = np.linspace(-10, 10, 1000)
x_vals = 1 - y_vals**2 / 12  # y^2 = -12(x-1) => x = 1 - y^2/12

# 각 점에서 (초점까지 거리) == (준선까지 거리) 확인
dist_focus = np.sqrt((x_vals - focus[0])**2 + (y_vals - focus[1])**2)
dist_directrix = np.abs(x_vals - k)

if np.allclose(dist_focus, dist_directrix, atol=1e-9):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
