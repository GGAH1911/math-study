import numpy as np
from math import sqrt, floor

# f(x) 정의: 주기 1인 주기함수
def f(x):
    # x를 [0, 1)로 정규화 (정수 부분 제거)
    frac = x - floor(x)
    if 0 < frac < 1:
        return 3
    elif frac == 0 or abs(frac - 1) < 1e-10:
        # 정수이거나 거의 정수: 원래 (0,1]에서 x=1일 때 f(1)=1
        if abs(frac) < 1e-10 or abs(frac - 1) < 1e-10:
            # x가 정수일 때: f(n) = f(0+) = 1로 정의 (x=1 경계값)
            # 하지만 주기성으로 f(n) = f(n mod 1) = f(0) = 1
            return 1
    return 3

# 더 명확한 정의
def f_clear(x):
    # 구간 (0,1]에서 정의, 주기 1
    k = floor(x)
    frac = x - k
    if abs(frac) < 1e-10:  # frac == 0 (x가 정수)
        return 1
    elif 0 < frac < 1:
        return 3
    else:  # frac == 1 (거의 일어나지 않음)
        return 1

# 다시 생각: sqrt(k)의 소수부분 확인
def f_periodic(x):
    frac = x - int(x)  # 소수 부분
    if abs(frac) < 1e-10:  # 정수
        return 1
    elif 0 < frac < 1:
        return 3
    return 1

total = 0
for k in range(1, 21):
    sqrt_k = sqrt(k)
    f_val = f_periodic(sqrt_k)
    term = k * f_val / 3
    total += term

print(f"Calculated sum: {total}")
if abs(total - 190) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')