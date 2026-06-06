import numpy as np
from scipy.optimize import fsolve
from scipy.integrate import quad

# f(2f(x)) = 2x for x >= 1
# f(1)=1, f(2)=2, f(4)=4, f(8)=8
# Check: compute integral from 1 to 8 of x*f'(x)dx

# Using the formula: integral of x*f'(x)dx = [x*f(x)] - integral of f(x)dx
# = 8*f(8) - 1*f(1) - integral of f(x)dx
# = 64 - 1 - (5/4 + 7 + 20)
# = 63 - 113/4 = 252/4 - 113/4 = 139/4

integral_1_2 = 5/4
integral_2_4 = 7
integral_4_8 = 20

total_integral = integral_1_2 + integral_2_4 + integral_4_8
xfprime_integral = 8*8 - 1*1 - total_integral

expected = 139/4

if abs(xfprime_integral - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {xfprime_integral}, expected {expected}')