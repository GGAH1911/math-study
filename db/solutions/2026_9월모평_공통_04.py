import numpy as np

# 그래프를 그대로 코드화
# 곡선 부분: (-2,3), (-1,0), (0,-1)을 모두 지나는 가장 단순한 곡선 = x^2 - 1
# (검증: (-2)^2-1=3 ✓, (-1)^2-1=0 ✓, 0^2-1=-1 ✓)
# 직선 1: (0,1) -> (1,0): y = -x + 1
# 직선 2: (1,2) -> (2,3): y = x + 1

def f(x):
    if -2 <= x < 0:
        return x*x - 1
    elif x == 0:
        return 0  # 임의값 (극한 계산에 무관)
    elif 0 < x <= 1:
        return -x + 1
    elif 1 < x <= 2:
        return x + 1
    else:
        raise ValueError('out of domain')

# 좌극한 x -> 0-
lim_left_0 = None
vals = [f(-10.0**(-k)) for k in range(3, 12)]
lim_left_0 = vals[-1]
# 수렴 확인
assert all(abs(v - (-1)) < 1e-4 for v in vals[-3:]), f'left limit not converging: {vals}'

# 우극한 x -> 1+
lim_right_1 = None
vals2 = [f(1 + 10.0**(-k)) for k in range(3, 12)]
lim_right_1 = vals2[-1]
assert all(abs(v - 2) < 1e-4 for v in vals2[-3:]), f'right limit not converging: {vals2}'

total = lim_left_0 + lim_right_1
answer_candidate = 1

if abs(total - answer_candidate) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
