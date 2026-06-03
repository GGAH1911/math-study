import math
PI = math.pi

def evaluate(e1, e2, e3):
    eps = [1, e1, e2, e3]
    c = [0]
    for n in range(4):
        c.append(c[-1] + eps[n] * 2)
    def f(x):
        for n in range(4):
            if n*PI - 1e-12 <= x <= (n+1)*PI + 1e-12:
                t = max(0.0, min(PI, x - n*PI))
                return c[n] + eps[n] * (1 - math.cos(t))
        return 0.0
    # (가) check
    for x in [0.0, 0.7, 1.3, 2.1, 2.9, PI]:
        if abs(f(x) - (1 - math.cos(x))) > 1e-9:
            return None
    # (나) check
    for n in (1, 2, 3):
        for t in [0.4, 1.1, 2.3, PI]:
            lhs = f(n*PI + t)
            fnpi = f(n*PI); ft = f(t)
            if not (abs(lhs - fnpi - ft) < 1e-9 or abs(lhs - fnpi + ft) < 1e-9):
                return None
    # (다) count inflections
    interior = 4
    boundary = sum(1 for n in (1,2,3) if eps[n] == eps[n-1])
    if interior + boundary != 6:
        return None
    # integrate |f|
    N = 40000
    a, b = 0.0, 4*PI
    h = (b - a) / N
    s = 0.5 * (abs(f(a)) + abs(f(b)))
    for i in range(1, N):
        s += abs(f(a + i*h))
    return s * h

best = float('inf')
for e1 in (1, -1):
    for e2 in (1, -1):
        for e3 in (1, -1):
            v = evaluate(e1, e2, e3)
            if v is not None and v < best:
                best = v
expected = 6 * PI
if abs(best - expected) < 0.01:
    print('VERIFY_PASS')
else:
    print(f'got {best}, expected {expected}')
    print('VERIFY_FAIL')
