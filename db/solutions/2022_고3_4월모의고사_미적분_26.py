import numpy as np

def f_analytical(x):
    u = x / 2
    abs_u = abs(u)
    if abs_u < 1:
        return -1.0
    elif abs_u > 1:
        return 3.0 * u  # = 3x/2
    elif u > 0:  # u == 1, x == 2
        return 1.0
    else:  # u == -1, x == -2
        return -2.0

# Verify claimed solutions
k_solutions = [-1.0, -2.0]
for k in k_solutions:
    val = f_analytical(k)
    if abs(val - k) > 1e-9:
        print('VERIFY_FAIL'); exit()

# Verify no extra solutions exist on a fine grid
for k in np.linspace(-20, 20, 200001):
    fval = f_analytical(k)
    if abs(fval - k) < 1e-3:
        already = any(abs(k - s) < 0.01 for s in k_solutions)
        if not already:
            print('VERIFY_FAIL'); exit()

total = sum(k_solutions)
if abs(total - (-3)) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')