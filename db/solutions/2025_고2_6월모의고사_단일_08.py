from math import log

def base(a):
    return -a*a - a + 7

valid = []
for a in range(-20, 21):
    b = base(a)
    if b <= 0 or b == 1:
        continue
    # 증가함수: 두 점 x1<x2 에서 log_b(x1) < log_b(x2)
    x1, x2 = 2.0, 3.0
    y1 = log(x1)/log(b)
    y2 = log(x2)/log(b)
    if y2 > y1:
        valid.append(a)

ans = sum(valid)
print('valid a =', valid, 'sum =', ans)
print('VERIFY_PASS' if ans == -2 else 'VERIFY_FAIL')
