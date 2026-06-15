import math
from sympy import sqrt, symbols, solve, simplify

# Define the function and its inverse
def f_inv(y):
    return (y**2 + 12) / 3

# g(x) = sqrt(6x - 12)
def g(x):
    return math.sqrt(6*x - 12)

# Verify the condition: f^{-1}(g(x)) = 2x for x=3
x_val = 3
g_val = g(x_val)
f_inv_g = f_inv(g_val)
expected = 2 * x_val

if abs(f_inv_g - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')