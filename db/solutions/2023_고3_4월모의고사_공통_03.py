import numpy as np

# 그래프에 따른 f(x) 정의
# x < -1: 좌측에서 (-1, 1)로 접근하는 직선 (예: y = -x, x<-1 이면 y>1)
# x = -1: f(-1) = 2 (채워진 점)
# -1 < x < 0: y = 2 (수평선분)
# x = 0: 열린 점 (정의 안 됨)
# 0 < x < 2: (0,0)에서 (2,3)까지의 직선, y = 1.5x
# x = 2: f(2) = 2 (채워진 점)
# x > 2: 감소하는 곡선

def f(x):
    if x < -1:
        return -x  # 임의의 좌측 직선, x=-1에서 1로 접근
    elif x == -1:
        return 2
    elif -1 < x < 0:
        return 2
    elif x == 0:
        return None  # 정의 안 됨
    elif 0 < x < 2:
        return 1.5 * x
    elif x == 2:
        return 2
    else:
        return 2 - (x - 2)**2  # 임의의 감소 곡선

# lim_{x -> -1+} f(x): 우측에서 접근
right_limit_neg1 = f(-1 + 1e-9)
# lim_{x -> 2-} f(x): 좌측에서 접근
left_limit_2 = f(2 - 1e-9)

total = right_limit_neg1 + left_limit_2
answer = 5

if abs(total - answer) < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
