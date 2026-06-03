import numpy as np

def f(x, a=8, b=5):
    if x <= -8:
        return 2**(x + a) + b
    else:
        return -(3**(x - 3)) + 8

def count_integers(k, a=8, b=5):
    # S1 = (b, 2^(a-8)+b] — range of f on (-inf, -8]
    s1_lo = float(b)
    s1_hi = float(2**(a - 8) + b)
    ints = set()
    for n in range(int(s1_lo) - 5, int(s1_hi) + 5):
        if s1_lo < n <= s1_hi:
            ints.add(n)
    # S2(k) = [f(k), sup) — range of f on (-8, k] if k > -8
    if k > -8:
        fk = f(k, a, b)
        sup_s2 = -(3**(-11)) + 8  # exclusive
        for n in range(-200, 200):
            if fk <= n < sup_s2:
                ints.add(n)
    return len(ints)

passed = True
# k in [3, 4): count must be 2
for k in [3.0, 3.1, 3.3, 3.0 + np.log(2)/np.log(3), 3.8, 3.99]:
    c = count_integers(k)
    if c != 2:
        print(f'FAIL at k={k:.4f}: count={c} expected 2')
        passed = False
# k < 3: count must not be 2
for k in [-100, -9, -8.001, -8.0, -1, 0, 1, 2, 2.99]:
    c = count_integers(k)
    if c == 2:
        print(f'FAIL at k={k}: count={c} expected != 2')
        passed = False
# k >= 4: count must not be 2
for k in [4.0, 4.5, 5.0, 10.0]:
    c = count_integers(k)
    if c == 2:
        print(f'FAIL at k={k}: count={c} expected != 2')
        passed = False
print('VERIFY_PASS' if passed else 'VERIFY_FAIL')