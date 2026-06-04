import numpy as np

def count_intersections(a, b):
    count = 0
    for rhs in [1, -1]:
        target = (rhs - b) / 2.0
        if abs(target) > 1.0 + 1e-12:
            continue
        target = max(-1.0, min(1.0, target))
        arc = np.arcsin(target)
        sol1 = arc % (2 * np.pi)
        sol2 = (np.pi - arc) % (2 * np.pi)
        bases = set()
        bases.add(round(sol1, 9))
        diff = abs(sol1 - sol2)
        if diff > 1e-9 and abs(diff - 2*np.pi) > 1e-9:
            bases.add(round(sol2, 9))
        for sol_base in bases:
            k_min = int(np.ceil(-sol_base / (2*np.pi) - 1e-9))
            k_max = int(np.floor((2*a*np.pi - sol_base) / (2*np.pi) + 1e-9))
            for k in range(k_min, k_max + 1):
                t = sol_base + 2*np.pi*k
                if -1e-9 <= t <= 2*a*np.pi + 1e-9:
                    count += 1
    return count

pairs = []
for a in range(1, 30):
    for b in range(1, 30):
        if count_intersections(a, b) == 10:
            pairs.append((a, b, a+b))

if pairs:
    sums = [p[2] for p in pairs]
    M = max(sums)
    m = min(sums)
    if M + m == 17:
        print('VERIFY_PASS')
    else:
        print(f'VERIFY_FAIL: M+m={M+m}, pairs={pairs}')
else:
    print('VERIFY_FAIL: no pairs found')
