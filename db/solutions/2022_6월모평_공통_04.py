import numpy as np

# Left piece: f(x) = -x - 2 for x <= 0
# Right piece: f(x) = x - 2 for x > 2

eps = 1e-9

# lim_{x->0-}: approach 0 from the left using f(x) = -x - 2
x_vals_left = np.array([-eps, -1e-6, -1e-3])
f_left = -x_vals_left - 2
lim_0_minus = f_left[0]  # should be -2

# lim_{x->2+}: approach 2 from the right using f(x) = x - 2
x_vals_right = np.array([2 + eps, 2 + 1e-6, 2 + 1e-3])
f_right = x_vals_right - 2
lim_2_plus = f_right[0]  # should be 0

result = lim_0_minus + lim_2_plus
expected = -2

if abs(result - expected) < 1e-6:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: got {result}, expected {expected}')
