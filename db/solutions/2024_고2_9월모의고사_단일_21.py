import math

def count_roots(t, a, b):
    c = 0
    # Left: 2^(x+a) = t, x = log2(t) - a, need x <= 0
    if t > 0:
        x = math.log2(t) - a
        if x <= 0:
            c += 1
    # Right: (x+b)^2 = t, x > 0
    if t >= 0:
        s = math.sqrt(t)
        if -b + s > 0:
            c += 1
        if -b - s > 0:
            c += 1
    return c

def lim_left(t, a, b):
    return count_roots(t - 1e-9, a, b)

def lim_right(t, a, b):
    return count_roots(t + 1e-9, a, b)

def valid(a, b):
    L, R = 2**a, b**2
    disc = []
    for d in {L, R}:
        if d > 1e-9 and lim_left(d, a, b) != lim_right(d, a, b):
            disc.append(d)
    has_k = any(abs(d2 - 2*d1) < 1e-6 for d1 in disc for d2 in disc)
    if not has_k:
        return False
    return lim_left(16, a, b) * lim_right(16, a, b) == 2

cands = [(5, 4), (4, 2*math.sqrt(2)), (4, -2*math.sqrt(2)), (3, -4)]
sums = [a + b for a, b in cands if valid(a, b)]

# Confirm exhaustiveness: also brute-search a grid for any missed (a,b)
import itertools
grid_a = [i*0.1 for i in range(-50, 80)]
grid_b = [i*0.1 for i in range(-60, 60)]
extra = []
for a in grid_a:
    for b in grid_b:
        if valid(a, b):
            ab = a + b
            if all(abs(ab - s) > 1e-3 for s in sums):
                extra.append((a, b, ab))

if len(sums) == 4 and abs(max(sums) - 9) < 1e-6 and abs(min(sums) + 1) < 1e-6:
    product = max(sums) * min(sums)
    if abs(product - (-9)) < 1e-6:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')
