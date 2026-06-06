import numpy as np
from scipy.optimize import fsolve

k = -3

def f(x):
    return x**3 + x**2 - x

def g(x):
    return 4*np.abs(x) + k

# Check intersection points
x_points = [-1, 1]
for x in x_points:
    f_val = f(x)
    g_val = g(x)
    assert abs(f_val - g_val) < 1e-10, f'Not equal at x={x}'

# Verify area
from scipy.integrate import quad

def integrand_left(x):
    return f(x) - g(x)

def integrand_right(x):
    return f(x) - g(x)

area_left, _ = quad(integrand_left, -1, 0)
area_right, _ = quad(integrand_right, 0, 1)

S = area_left + area_right
result = 30 * S

assert abs(result - 80) < 1e-6, f'Area calculation failed: {result}'
print('VERIFY_PASS')