import math

def f(x):
    if x < -1:
        return -x + 1          # 기울기 -1, 열린원 (-1,2)
    elif x <= 0:               # -1 <= x <= 0
        return -1              # 상수 -1
    elif x < 1:                # 0 < x < 1
        return 2*x - 1         # 기울기 2
    elif abs(x - 1) < 1e-12:
        return -1              # f(1) = -1
    else:                      # x > 1
        return -2*x + 1        # 감소 직선, (1,-1) 통과: -2*1+1=-1 ✓

eps = 1e-8

# 극한1: lim_{x->0+} f(x-1) = lim_{t->-1+} f(t)
t = -1 + eps
limit1 = f(t)  # 상수 구간이므로 -1

# 극한2: lim_{x->1+} f(f(x))
x = 1 + eps
fx = f(x)          # f(x) = -2(1+eps)+1 = -1-2eps < -1
ffx = f(fx)        # f(-1-2eps) = -(-1-2eps)+1 = 2+2eps -> 2

total = limit1 + ffx  # -1 + 2 = 1

CANDIDATE = 1

if math.isclose(total, CANDIDATE, abs_tol=1e-4):
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {total}, expected {CANDIDATE}')
