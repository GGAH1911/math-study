import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar

def f(x):
    def integrand(t):
        return np.abs(2**t - 5)
    result, _ = quad(integrand, x, x+2)
    return result

result = minimize_scalar(f, bounds=(-1, 4), method='bounded')
m = result.fun
power_2_m = 2**m
expected = (5/4)**10

if abs(power_2_m - expected) / expected < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')