import numpy as np
from scipy.optimize import fsolve

a, b = 4, 4

def f(x):
    return a * np.sin(b*x) + 8 - a

# Check condition (가): f(x) >= 0 for all x
min_val = -a + (8 - a)  # minimum of a*sin(bx) + 8 - a
assert min_val >= 0, f"Condition (가) failed: min value = {min_val}"

# Check condition (나): exactly 4 roots in [0, 2π)
roots = []
for k in range(10):
    x_candidate = (3*np.pi/2 + 2*np.pi*k) / b
    if 0 <= x_candidate < 2*np.pi:
        roots.append(x_candidate)
        
assert len(roots) == 4, f"Condition (나) failed: found {len(roots)} roots instead of 4"

# Verify roots satisfy f(x) = 0
for root in roots:
    val = f(root)
    assert abs(val) < 1e-10, f"f({root}) = {val} != 0"

print('VERIFY_PASS')