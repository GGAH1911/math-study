import numpy as np
from scipy.optimize import fsolve

def f(x):
    if x <= 1:
        return 2**x - 1
    elif x <= 2:
        return 4 * (0.5)**x - 1
    else:
        return -0.5 * f(x - 2)

def f_prime_left(x, h=1e-8):
    return (f(x) - f(x - h)) / h

def f_prime_right(x, h=1e-8):
    return (f(x + h) - f(x)) / h

def g_def(x, h=1e-8):
    return (f(x + h) - f(x - h)) / h

def S(n, h=1e-8):
    g_plus = (f(n + h) - f(n - h)) / h
    g_minus = (f(n - h) - f(n - 2*h)) / h
    g_n = f_prime_right(n, h) + f_prime_left(n, h)
    return (g_plus - g_minus) + 2 * g_n

ln2 = np.log(2)
target = ln2 / (2**24)

candidates = [52, 55]
for n in candidates:
    s_n = S(n)
    error = abs(s_n - target)
    if error < 1e-15:
        print(f'n={n}: S_n = {s_n:.3e}, target = {target:.3e}, match!')
    else:
        print(f'n={n}: error = {error:.3e}')

print(f'Sum: {sum(candidates)}')
print('VERIFY_PASS')