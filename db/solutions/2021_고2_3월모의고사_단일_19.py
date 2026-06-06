import numpy as np
from sympy import symbols, solve, Min, Max

n = 12
x_vals = np.linspace(2, 5, 1000)
f_vals = x_vals**2 - 8*x_vals + n

max_f = np.max(f_vals)
if max_f >= 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')