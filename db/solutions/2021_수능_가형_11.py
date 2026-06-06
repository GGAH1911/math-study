import numpy as np

def riemann_sum(n):
    k = np.arange(1, n+1)
    term = np.sqrt(3*n / (3*n + k))
    return np.sum(term) / n

expected = 4*np.sqrt(3) - 6
n = 100000
computed = riemann_sum(n)

if abs(computed - expected) < 1e-4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')