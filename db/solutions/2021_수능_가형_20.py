import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

n = 16

def g(x):
    nx = n * x
    frac_part = nx - np.floor(nx)
    return 1.0 if frac_part < 0.5 else 0.0

def h(x):
    return np.pi * np.sin(2 * np.pi * n * x) * g(x)

def integrand1(x):
    return h(x)

def integrand2(x):
    return x * h(x)

int1, _ = quad(integrand1, -1, 1, limit=100)
int2, _ = quad(integrand2, -1, 1, limit=100)

if abs(int1 - 2) < 1e-6 and abs(int2 - (-1/32)) < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'int1={int1}, expected=2')
    print(f'int2={int2}, expected={-1/32}')