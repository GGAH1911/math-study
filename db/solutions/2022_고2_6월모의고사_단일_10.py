import numpy as np

a, b, c = 2, 3, -1

def f(x):
    return a * np.cos(b * x) + c

# 원래 함수 조건 검증
max_val = a + c   # 이론적 최대
min_val = -a + c  # 이론적 최소

# 최댓값 = 1, 최솟값 = -3 확인
cond1 = abs(max_val - 1) < 1e-9
cond2 = abs(min_val - (-3)) < 1e-9

# x = pi/3 에서 최솟값(-3) 확인
cond3 = abs(f(np.pi/3) - (-3)) < 1e-9

# x = 2pi/3 에서 최댓값(1) 확인
cond4 = abs(f(2*np.pi/3) - 1) < 1e-9

# a*b*c = -6 확인
cond5 = abs(a * b * c - (-6)) < 1e-9

if all([cond1, cond2, cond3, cond4, cond5]):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
