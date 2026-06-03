import numpy as np

def f(x):
    if x <= -1:
        return -x - 1  # 직선, f(-1) = 0
    elif -1 < x < 0:
        return x + 2  # 곡선 근사: (-1,1)→(0,2) 선형
    elif x == 0:
        return 3
    elif 0 < x < 1:
        return 3 - 2 * x  # 직선: (0,3)→(1,1)
    elif x == 1:
        return 3
    else:  # x > 1
        return 3 + 1.5 * (x - 1)  # 증가 직선, (1,3)에서 시작

epsilon = 1e-9
left_0 = f(0 - epsilon)    # lim_{x→0-} f(x)
right_1 = f(1 + epsilon)   # lim_{x→1+} f(x)

total = left_0 + right_1

if abs(left_0 - 2) < 1e-6 and abs(right_1 - 3) < 1e-6 and abs(total - 5) < 1e-6:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: left_0={left_0}, right_1={right_1}, total={total}')
