import numpy as np

# 그래프에서 읽은 함수 f(x) 정의
# x < -1: 증가하는 곡선, x=-1에서 f(-1)=3 (닫힌 점)
# -1 < x < 1: (-1, 2) 열린점에서 시작해 (0,0) 통과 후 (1,1) 열린점으로 향하는 곡선
#   이 구간을 y = x^2 로 모델링하면 좌극한(-1+)=1이 아니라 1이 되는데,
#   그래프상 (-1, 2) 열린점이므로 실제 구간 함수는 y = x^2 + (보정) 형태.
#   그래프에서 x=-1+ -> 2, x=0 -> 0, x=1- -> 1 을 만족해야 함.
# 실제로 그래프의 형태(좌우 비대칭 곡선)는 중요하지 않고, 열린 점 좌표가 극한값.

def f(x):
    if x < -1:
        return 4 * x + 7  # 좌측 직선/곡선 (x=-1에서 3)
    elif x == -1:
        return 3  # 닫힌 점
    elif -1 < x < 1:
        # (-1+, 2), (0, 0), (1-, 1)을 지나는 곡선
        # 이차함수로 보간: y = a*x^2 + b*x + c
        # f(-1) = 2 (극한): a - b + c = 2
        # f(0) = 0: c = 0
        # f(1) = 1 (극한): a + b + c = 1
        # => a - b = 2, a + b = 1 => a = 1.5, b = -0.5
        return 1.5 * x**2 - 0.5 * x
    elif x == 1:
        return 2  # 닫힌 점
    else:  # x > 1
        return 2

# 우극한 x -> -1+
right_limit_neg1 = f(-1 + 1e-9)
# 좌극한 x -> 1-
left_limit_pos1 = f(1 - 1e-9)

total = right_limit_neg1 + left_limit_pos1

if abs(total - 3) < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
