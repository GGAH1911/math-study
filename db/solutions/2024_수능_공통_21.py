import math

# a = 10일 때 검증
a = 10

# g(t)의 최솟값이 5인지 확인
# 핵심 점들에서의 g(t) 값 계산

def f(x):
    if -1 <= x < 6:
        return -x**2 + 6*x
    elif x >= 6:
        return a * math.log(x-5) / math.log(4)
    return None

def g_value(t):
    # [t-1, t+1] 구간에서 f(x)의 최댓값
    if t < 2:
        # [t-1, t+1] 내 최댓값
        return -(t**2) + 4*t + 5
    elif t <= 4:
        return 9
    elif t <= 5:
        return -(t**2) + 8*t - 7
    elif t < 7:
        h1 = -(t**2) + 8*t - 7
        h2 = a * math.log(t-4) / math.log(4)
        return max(h1, h2)
    else:
        return a * math.log(t-4) / math.log(4)

# 최솟값 확인
min_val = float('inf')
min_t = None
for t in [0, 6, 7]:
    g_t = g_value(t)
    if g_t < min_val:
        min_val = g_t
        min_t = t

# 더 세밀한 탐색
for t_test in [0, 0.5, 1, 2, 3, 4, 5, 6, 6.5, 7, 8]:
    g_t = g_value(t_test)
    if g_t < min_val:
        min_val = g_t
        min_t = t_test

if abs(min_val - 5.0) < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')