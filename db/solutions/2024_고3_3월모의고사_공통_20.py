import numpy as np
from numpy import cos, pi

def f(x):
    return 2*x**2 + 2*x - 1

def g(x):
    return cos(pi/3 * x)

# Check all solutions
solutions = [1, 3, 5, 7, 9, 11]
all_valid = True

for x in solutions:
    g_val = g(x)
    f_g_val = f(g_val)
    if abs(f_g_val - g_val) > 1e-10:
        all_valid = False
        break

if all_valid and sum(solutions) == 36:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')