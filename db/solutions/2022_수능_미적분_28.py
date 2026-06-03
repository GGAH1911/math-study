import numpy as np

def f(x):
    return 6*np.pi*(x-1)**2

def g(x):
    return 3*f(x) + 4*np.cos(f(x))

def gp(x):
    return 12*np.pi*(x-1) * (3 - 4*np.sin(f(x)))

# 원래 함수 g(x) 자체로부터 극소의 개수를 셈 (수치 미분 부호 변화)
xs = np.linspace(1e-8, 2-1e-8, 4_000_001)
gps = gp(xs)

# 부호 변화: 음 -> 양으로 바뀌는 횟수 = 극소 개수
count = 0
prev_sign = 0
for s in gps:
    cur = 1 if s > 0 else (-1 if s < 0 else 0)
    if cur == 1 and prev_sign == -1:
        count += 1
    if cur != 0:
        prev_sign = cur

# 교차 검증: 실제 g 값으로 극소 직접 카운트
ys = g(xs)
dy = np.diff(ys)
count2 = int(np.sum((dy[:-1] < 0) & (dy[1:] > 0)))

expected = 7
if count == expected and count2 == expected:
    print('VERIFY_PASS')
else:
    print(f'g\'-sign count={count}, g-value count={count2}, expected={expected}')
    print('VERIFY_FAIL')
