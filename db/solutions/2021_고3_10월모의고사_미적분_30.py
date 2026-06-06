import numpy as np
from scipy.optimize import fsolve

# a = 1/2, b = 3
a, b = 0.5, 3

def f(x):
    return -(a*x**3 + b*x) / (x**2 + 1)

def f_prime(x):
    return -(a*x**4 + (3*a - b)*x**2 + b) / (x**2 + 1)**2

# Verify f(2) = -2
assert abs(f(2) - (-2)) < 1e-10, f"f(2) = {f(2)}, expected -2"

# Verify f(-2) = 2
assert abs(f(-2) - 2) < 1e-10, f"f(-2) = {f(-2)}, expected 2"

# Verify 4a + b = 5
assert abs(4*a + b - 5) < 1e-10, f"4a + b = {4*a + b}, expected 5"

# Verify f'(2) = -1/5
assert abs(f_prime(2) - (-0.2)) < 1e-10, f"f'(2) = {f_prime(2)}, expected -0.2"

# Verify conditions (가) and (나)
# (가): g(2) = h(0)
# f^{-1}(2) = -2 (since f(-2) = 2)
g_2 = f(2) - (-2)
h_0 = f(f(0))
assert abs(g_2 - h_0) < 1e-10, f"g(2)={g_2}, h(0)={h_0}"

# (나): g'(2) = -5h'(2)
# g'(2) = f'(2) - 1/f'(f^{-1}(2)) = f'(2) - 1/f'(-2)
g_prime_2 = f_prime(2) - 1/f_prime(-2)
h_prime_2 = f_prime(f(2)) * f_prime(2) - 1
assert abs(g_prime_2 - (-5*h_prime_2)) < 1e-10, f"g'(2)={g_prime_2}, -5h'(2)={-5*h_prime_2}"

print("VERIFY_PASS")