import numpy as np

def count_intersections(k, a):
    if a < -1e-12:
        return 0
    roots = []
    for sign in (1, -1):
        coeffs = [1.0, 0.0, -12.0, k - sign * a]
        for r in np.roots(coeffs):
            if abs(r.imag) < 1e-6:
                roots.append(r.real)
    unique = []
    for r in sorted(roots):
        if not unique or abs(r - unique[-1]) > 1e-4:
            unique.append(r)
    return len(unique)

def num_odd_a(k):
    g_m2 = (-2)**3 - 12*(-2) + k
    g_p2 = 2**3 - 12*2 + k
    crit = sorted({0.0, abs(g_m2), abs(g_p2)})
    # Ensure intervals between/above critical a values are all even (no interval odd-count)
    sample = [(crit[i] + crit[i+1]) / 2 for i in range(len(crit)-1)] + [crit[-1] + 10.0]
    for a in sample:
        if count_intersections(k, a) % 2 == 1:
            return float('inf')
    return sum(1 for a in crit if count_intersections(k, a) % 2 == 1)

k = 16
ok = (num_odd_a(k) == 1)
for k_other in (8, 10, 12, 14):
    if num_odd_a(k_other) == 1:
        ok = False
        break
print('VERIFY_PASS' if ok else 'VERIFY_FAIL')
