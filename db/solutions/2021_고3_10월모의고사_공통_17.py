import numpy as np
from scipy import integrate

# 속도 함수
def v(t):
    return 12 - 4*t

# t=0에서 t=3까지 적분 (양의 방향)
dist1, _ = integrate.quad(v, 0, 3)

# t=3에서 t=4까지 적분 (음의 방향)
dist2, _ = integrate.quad(v, 3, 4)

# 움직인 거리 (속도의 절댓값을 적분)
total_distance, _ = integrate.quad(lambda t: abs(v(t)), 0, 4)

if abs(total_distance - 20.0) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')