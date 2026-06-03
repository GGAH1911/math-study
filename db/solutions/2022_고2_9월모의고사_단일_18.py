import numpy as np

pi = np.pi
k = 2/9

def f(x):
    return abs(np.sin(2*x) + 2/3)

def find_roots_sin_eq(c, lo=-pi, hi=pi):
    if abs(c) > 1:
        return []
    t = np.arcsin(c)
    cands = []
    for base in [t, pi - t]:
        for shift in [-4*pi, -2*pi, 0, 2*pi, 4*pi]:
            x = (base + shift) / 2
            if lo - 1e-12 <= x <= hi + 1e-12:
                cands.append(x)
    # deduplicate
    cands = sorted(set(round(v, 12) for v in cands))
    return cands

# f(x)=k roots: sin(2x)=k-2/3 or sin(2x)=-k-2/3
c1 = k - 2/3    # -4/9
c2 = -k - 2/3   # -8/9
roots = find_roots_sin_eq(c1) + find_roots_sin_eq(c2)

# m = N(3k), 3k=2/3: sin(2x)=0 gives 5 roots; sin(2x)=-4/3 no solution
roots_3k = find_roots_sin_eq(3*k - 2/3) + find_roots_sin_eq(-3*k - 2/3)
m = len(roots_3k)
n = len(roots)

# checks
root_ok = all(abs(f(r) - k) < 1e-9 for r in roots)
sum_ok = abs(sum(roots) - 2*pi) < 1e-9
mn_ok = abs(m - n) == 3
count_ok = (n == 8 and m == 5)

if root_ok and sum_ok and mn_ok and count_ok:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    if not root_ok: print('root check failed')
    if not sum_ok: print(f'sum={sum(roots):.6f}, expected {2*pi:.6f}')
    if not mn_ok: print(f'|m-n|={abs(m-n)}, expected 3')
    if not count_ok: print(f'n={n}, m={m}')
