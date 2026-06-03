import numpy as np

k = 2

# f(x) = (x-1)^2 - 5 (axis x=3-k=1, c=1-k-k^2=-5)
def f(x):
    return (x - 1)**2 - 5

def g(x):
    return (f(x) + k) / np.exp(f(x))

# Check 1: f(3-2k) == f(3)
cond1 = np.isclose(f(3 - 2*k), f(3))

# Check 2: g(3) == e
cond2 = np.isclose(g(3), np.e)

# Check 3: x=3 is local max (g' changes + to -)
eps = 1e-6
def g_prime_num(x):
    return (g(x + eps) - g(x - eps)) / (2 * eps)

cond3 = (g_prime_num(3 - 0.01) > 0) and (g_prime_num(3 + 0.01) < 0)

# Check 4: g(k) = g(2) = -2e^4
g_k = g(k)
expected = -2 * np.exp(4)
cond4 = np.isclose(g_k, expected, rtol=1e-9)

if cond1 and cond2 and cond3 and cond4:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: cond1={cond1}, cond2={cond2}, cond3={cond3}, cond4={cond4}, g(k)={g_k}, expected={expected}')
