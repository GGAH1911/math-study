import numpy as np
from scipy import integrate

CANDIDATE = 10

def f(x):
    return x + np.abs(x - 3)

# Numerical integration
result, _ = integrate.quad(f, 1, 4)

# Analytical calculation
part1 = 3 * (3 - 1)  # integral of 3 from 1 to 3
part2 = (4**2 - 3*4) - (3**2 - 3*3)  # [x^2 - 3x] from 3 to 4
analytical = part1 + part2

if abs(result - CANDIDATE) < 1e-6 and abs(analytical - CANDIDATE) < 1e-6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')