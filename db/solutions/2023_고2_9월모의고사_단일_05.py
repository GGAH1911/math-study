import numpy as np

# 원래 문제의 그래프를 함수로 구현
# x<1: 감소하는 곡선, x->1- 일 때 2로 접근 (예: 1/x + 1 형태로 (1,2)에 도달)
# 1<x<3: V자, 꼭짓점 (2,0), 양 끝 (1,1), (3,1)에서 |x-2|
# x>3: (3,3)에서 시작해 감소하는 직선, 기울기 -6 정도 (예: -6(x-3)+3)

def f(x):
    if x < 1:
        return 1.0/x + 1.0  # x->1- 일 때 2로 접근
    elif x == 1:
        return 2.0  # 채워진 점
    elif x < 3:
        return abs(x - 2.0)  # V자, x->1+ 일 때 1, x->3- 일 때 1
    elif x == 3:
        return 1.0  # 채워진 점
    else:
        return -6.0*(x - 3.0) + 3.0  # x->3+ 일 때 3으로 접근

# 좌극한 x->1-
lim_left = f(1 - 1e-9)
# 우극한 x->3+
lim_right = f(3 + 1e-9)

total = lim_left + lim_right

if abs(total - 5) < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
