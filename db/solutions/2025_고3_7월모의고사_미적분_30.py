import numpy as np
from scipy.integrate import quad, odeint

# f(x) = integral from 0 to x of e^(cos(pi*t)) dt
def f(x):
    result, _ = quad(lambda t: np.exp(np.cos(np.pi*t)), 0, x)
    return result

# Numerical verification
A = f(1)
print(f'A = f(1) = {A}')

# h(u) = 2(f(u-2))^3 + 6A(f(u-2))^2 + 1
def h(u):
    fu2 = f(u - 2) if u >= 2 else (f(u - 2) if u > -2 else 0)
    return 2 * fu2**3 + 6 * A * fu2**2 + 1

# h'(x) = 6*f(x-2)*[f(x-2) + 2A] * e^(cos(pi*x))
def h_prime(x):
    fx2 = f(x - 2)
    return 6 * fx2 * (fx2 + 2*A) * np.exp(np.cos(np.pi*x))

# Compute integral
integral, _ = quad(lambda x: h_prime(x) / f(x), 3, 7)
k = integral / (A**2)
print(f'integral / A^2 = {k}')
print(f'Expected k = 72')
if abs(k - 72) < 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')