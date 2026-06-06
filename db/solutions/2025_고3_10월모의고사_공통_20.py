import numpy as np
from scipy.optimize import fsolve

# Case 1: 2^a = 3/2
a1 = np.log2(3/2)
f_min_1 = 10 - 4 * (3/2)
t_min_g_1 = 10 * (3/2) - 4 * (3/2)**2 - 2
assert abs(f_min_1 - t_min_g_1) < 1e-10, f'Case 1 failed: {f_min_1} != {t_min_g_1}'

# Case 2: 2^a = 2
a2 = 1
f_min_2 = 10 - 4 * 2
t_min_g_2 = 10 * 2 - 4 * 4 - 2
assert abs(f_min_2 - t_min_g_2) < 1e-10, f'Case 2 failed: {f_min_2} != {t_min_g_2}'

# Product of all 2^a
product = (3/2) * 2
assert abs(product - 3) < 1e-10, f'Product calculation failed: {product}'

print('VERIFY_PASS')