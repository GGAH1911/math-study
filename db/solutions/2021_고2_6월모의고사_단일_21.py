import math

def f(x, k=-1.5):
    if x < k:
        return 2**(x-2) - 2
    else:
        return -math.log2(x+2) - 2

def g(x, k=-1.5):
    if x < -k:
        return math.log2(2-x) + 2
    else:
        return -2**(x-2) + 2

k = -1.5
count = 0

for a in range(-2, 3):
    fa = f(a, k)
    ga = g(a, k)
    
    # f(a) <= b <= g(a)를 만족하는 정수 b의 개수
    if fa <= ga:
        b_min = math.ceil(fa)
        b_max = math.floor(ga)
        count += max(0, b_max - b_min + 1)

if count == 31:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {count}')