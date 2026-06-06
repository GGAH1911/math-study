import numpy as np
from scipy.optimize import fsolve

def f(x):
    return np.sin(x)

def g(x):
    return -np.cos(x) + (1 - np.sqrt(3))/2

def h(x):
    return np.maximum(f(x), g(x))

k = (3 - np.sqrt(3))/2

# Find roots of h(x) = k in [0, 2π]
roots = []
for x0 in np.linspace(0, 2*np.pi, 50):
    try:
        root = fsolve(lambda x: h(x) - k, x0, full_output=True)
        if root[2] == 1:  # Solution found
            r = root[0][0] % (2*np.pi)
            if 0 <= r <= 2*np.pi and not any(abs(r - rr) < 1e-6 for rr in roots):
                roots.append(r)
    except:
        pass

if len(roots) == 3:
    # Verify each root
    all_valid = all(abs(h(r) - k) < 1e-9 for r in roots)
    if all_valid:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')