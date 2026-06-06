import numpy as np
from scipy.optimize import fsolve

# u = 1/2 검증
u = 0.5
eq = 4*u**3 - 7*u + 3
if abs(eq) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')