import numpy as np

def f(x):
    return np.cos(x)**2 - np.sin(x) - 1

p = 3*np.pi/2

# 1) f(p) = 0
fp = f(p)

# 2) f > 0 on (pi, p) => infimum=0 not attained => min doesn't exist for a < p
xs = np.linspace(np.pi + 1e-9, p - 1e-9, 1000000)
interior_min = np.min(f(xs))

# 3) M = max f on (pi, p]
xs2 = np.linspace(np.pi + 1e-9, p, 1000000)
M = np.max(f(xs2))

# 4) p * M == 3*pi/8
result = p * M
expected = 3*np.pi/8

if (abs(fp) < 1e-9 and
    interior_min > -1e-7 and
    abs(M - 0.25) < 1e-6 and
    abs(result - expected) < 1e-6):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
