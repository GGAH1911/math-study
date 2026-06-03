import math

def g(n):
    # phi(x)=3^x - x, larger root with x>=0 (phi(0)=1, increasing for x>x*~-0.086)
    lo, hi = 0.0, 1.0
    while 3**hi - hi - n < 0:
        hi *= 2
        if hi > 1000:
            break
    for _ in range(300):
        mid = (lo + hi) / 2
        if 3**mid - mid - n > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2

def h(n):
    return math.floor(g(n))

result = [n for n in range(2, 101) if h(n) < h(n+1)]
total = sum(result)
print(f'n values satisfying h(n)<h(n+1): {result}')
print(f'Sum: {total}')
if total == 105 and result == [6, 23, 76]:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
