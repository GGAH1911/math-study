import sympy as sp
from sympy import symbols, integrate, diff, solve

CANDIDATE = 9

# f(x) = 4x^3 - 18x^2 + c
x = symbols('x')
f = 4*x**3 - 18*x**2
f_prime = diff(f, x)

# g'(x) = -x*f'(x)
g_prime = -x * f_prime

# Verify g'(x) = -12x^2(x-3)
expected_g_prime = -12*x**2*(x-3)
assert sp.expand(g_prime - expected_g_prime) == 0, 'g_prime mismatch'

# Calculate integral
integral = integrate(g_prime, (x, 0, 1))
integral_value = int(integral)

if integral_value == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')