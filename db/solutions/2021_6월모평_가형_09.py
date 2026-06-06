import math
k = 4
m = -8

def f(x):
    return 2 * math.log(x + k, 0.5)

# 최댓값 확인 (x=0)
max_val = f(0)
if abs(max_val - (-4)) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')