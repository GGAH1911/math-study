import numpy as np

k = 16

def v(t):
    if 0 <= t <= 3:
        return -t**2 + t + 2
    else:
        return k * (t - 3) - 4

def x(t):
    if t <= 3:
        return -t**3/3 + t**2/2 + 2*t
    else:
        x3 = 1.5
        return x3 + k*(t-3)**2/2 - 4*(t-3)

# 두 번째 운동 방향 변화 시점
t2 = 3 + 4/k
pos_at_t2 = x(t2)

if abs(pos_at_t2 - 1) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')