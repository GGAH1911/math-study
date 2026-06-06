import numpy as np
from scipy.integrate import quad
from scipy.optimize import fminbound

def f(x):
    return x**3 - 12*x**2 + 45*x + 3

def f_prime(x):
    return 3*x**2 - 24*x + 45

def f_t_power4(t):
    return f(t)**4

def g_prime(x, a):
    if x == a:
        return 0
    integral, _ = quad(f_t_power4, a, x)
    return f_prime(x) * integral

def count_extrema(a):
    xs = np.linspace(a-5, a+10, 1000)
    g_prime_vals = [g_prime(x, a) for x in xs]
    sign_changes = 0
    for i in range(len(g_prime_vals)-1):
        if g_prime_vals[i] * g_prime_vals[i+1] < 0:
            sign_changes += 1
    return sign_changes

results = []
for a in [3, 5]:
    extrema = count_extrema(a)
    results.append((a, extrema))

print('VERIFY_PASS' if sum(a for a, e in results if e == 1) == 8 else 'VERIFY_FAIL')