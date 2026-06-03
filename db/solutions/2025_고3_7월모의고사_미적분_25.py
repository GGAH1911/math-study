import numpy as np

def f(x, N=10000):
    t = x / 5
    numerator = t**(N+1) + 2*x
    denominator = t**N + 1
    if np.isinf(t**N):
        # t > 1: divide by t^N
        return t  # = x/5
    return numerator / denominator

def f_exact(x):
    t = x / 5
    if 0 < t < 1:
        return 2 * x
    elif t == 1:
        return 11 / 2
    else:  # t > 1
        return x / 5

# Check k = 5/2
k1 = 5 / 2
fk1 = f_exact(k1)

# Check k = 25
k2 = 25.0
fk2 = f_exact(k2)

# Sum
total = k1 + k2  # should be 55/2 = 27.5

if abs(fk1 - 5) < 1e-9 and abs(fk2 - 5) < 1e-9 and abs(total - 55/2) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: f(5/2)={fk1}, f(25)={fk2}, sum={total}')
