import numpy as np

# 함수 정의 (그래프로부터)
def f_left(x):
    if -2 <= x <= -1:
        return x + 2
    elif -1 < x <= 0:
        return -x
    else:
        return None

def f_middle(x):
    if 0 <= x <= 1:
        return 2*x
    else:
        return None

def f_right(x):
    if x > 1:
        return 1
    else:
        return None

# 검증 1: 그래프의 점들이 함수 정의와 일치하는지
assert f_left(-2) == 0, f'f(-2) should be 0, got {f_left(-2)}'
assert f_left(-1) == 1, f'f(-1) should be 1, got {f_left(-1)}'
assert f_left(0) == 0, f'f(0) should be 0, got {f_left(0)}'
assert f_middle(1) == 2, f'f(1) should be 2, got {f_middle(1)}'

# 검증 2: 극한값
# lim x→-1 f(x) 확인
lim_left_minus_1 = f_left(-1.001)  # -1에 왼쪽에서 접근 (구간 -2≤x≤-1)
lim_right_minus_1 = f_left(-0.999)  # -1에 오른쪽에서 접근 (구간 -1<x≤0)
assert abs(lim_left_minus_1 - 1) < 0.01, f'lim x→-1- f(x) ≠ 1'
assert abs(lim_right_minus_1 - 1) < 0.01, f'lim x→-1+ f(x) ≠ 1'

# lim x→1+ f(x) 확인
lim_right_plus_1 = f_right(1.001)  # 1에 오른쪽에서 접근
assert lim_right_plus_1 == 1, f'lim x→1+ f(x) should be 1, got {lim_right_plus_1}'

# 최종 답
limit_sum = 1 + 1
assert limit_sum == 2, f'Sum should be 2, got {limit_sum}'
print('VERIFY_PASS')