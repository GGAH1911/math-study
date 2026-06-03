import numpy as np

def compute_g(n, pts=200000):
    a = (n - 1) * np.pi / 6
    b = (n + 2) * np.pi / 6
    x = np.linspace(a, b, pts)
    return float(np.max(np.abs(np.sin(x) - 0.5)))

# rational candidates at multiples of pi/6
RATIONAL = [0.0, 0.5, 1.0, 1.5]
IRRATIONAL_VAL = (1 + np.sqrt(3)) / 2  # ≈ 1.3660

def is_irrational(val, tol=1e-5):
    for r in RATIONAL:
        if abs(val - r) < tol:
            return False
    if abs(val - IRRATIONAL_VAL) < tol:
        return True
    return False  # unexpected value

irrational_ks = [k for k in range(1, 41) if is_irrational(compute_g(k))]
total = sum(irrational_ks)

if irrational_ks == [6, 11, 18, 23, 30, 35] and total == 123:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: irrational_ks={irrational_ks}, sum={total}')
