import numpy as np

def has_real_nth_root(m, n):
    # x^n = m  <=>  x^n - m = 0, solve original equation directly
    coeffs = [1] + [0]*(n-1) + [-m]
    roots = np.roots(coeffs)
    # a real root exists if some root has (near) zero imaginary part and x^n ~ m
    for r in roots:
        if abs(r.imag) < 1e-6:
            x = r.real
            if abs(x**n - m) < 1e-6 * (1 + abs(m)):
                return True
    return False

p = 0  # m > 0 count  (=> 'gaa')
q = 0  # m < 0 count  (=> 'naa')
for n in range(2, 11):
    for m in range(-(n-1), n):  # |m| from 1..n-1, both signs
        if m == 0:
            continue
        if not (1 <= abs(m) < n <= 10):
            continue
        if has_real_nth_root(m, n):
            if m > 0:
                p += 1
            else:
                q += 1

if p == 45 and q == 20 and (p + q) == 65:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
