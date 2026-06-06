import numpy as np
from scipy.integrate import quad

def v_part1(t):
    return 2*t**3 - 8*t

def v_part2(t):
    return 3*t**2 + 4*t - 20

# 거리 계산: |v(t)|를 0~3까지 적분
s1, _ = quad(lambda t: abs(v_part1(t)), 0, 2)
s2, _ = quad(lambda t: abs(v_part2(t)), 2, 3)
total_distance = s1 + s2

answer = 17
if abs(total_distance - answer) < 1e-6:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: expected {answer}, got {total_distance}')