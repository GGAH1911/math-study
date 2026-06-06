import sympy as sp
import numpy as np
from scipy.optimize import fsolve

a, b = 6, 3

def f(x):
    if x > a:
        return None
    return np.sqrt(-x + a) - b

def g(x):
    if x <= a:
        fx = np.sqrt(-x + a) - b
        return abs(fx) + b
    else:
        fx_val = np.sqrt(-(- x + 2*a) + a) - b
        return -fx_val + abs(b)

x_test = 150
g_150 = g(x_test)
result = g_150 ** 2

if abs(result - 36) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: g(150)^2 = {result}')