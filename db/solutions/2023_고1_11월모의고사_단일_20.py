import numpy as np
from sympy import *

t = symbols('t', positive=True)

# Circle with diameter AB: center (3,4), radius 2
# Line CD: x + 2y = 2t
# Distance from center to line
dist = Abs(3 + 2*4 - 2*t) / sqrt(5)

# Condition for intersection: dist <= 2
# |11 - 2t| <= 2*sqrt(5)
# (11 - 2*sqrt(5))/2 <= t <= (11 + 2*sqrt(5))/2
M = (11 + 2*sqrt(5)) / 2
m = (11 - 2*sqrt(5)) / 2
result = M - m

# Verify M - m = 2*sqrt(5)
expected = 2*sqrt(5)

if simplify(result - expected) == 0:
    # Also verify at boundary: distance = 2 (tangent)
    d_at_M = (Abs(11 - 2*M) / sqrt(5))
    d_at_m = (Abs(11 - 2*m) / sqrt(5))
    tol = 1e-10
    dM_val = float(d_at_M.evalf())
    dm_val = float(d_at_m.evalf())
    if abs(dM_val - 2) < tol and abs(dm_val - 2) < tol:
        # Verify intersection y-values are in [0, t] at boundaries
        for t_val in [float(M.evalf()), float(m.evalf())]:
            a5, b5 = 5, -4*(2*t_val - 1)
            c5 = (2*t_val - 3)**2 + 12
            disc = b5**2 - 4*a5*c5
            y_mid = -b5 / (2*a5)
            if disc >= -1e-10 and 0 <= y_mid <= t_val:
                continue
            else:
                print('VERIFY_FAIL')
                exit()
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')
