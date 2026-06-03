import numpy as np

# Derived constants
p = 0
q = 3
a = 3 - np.log2(3)  # = 3 - log2(3)

def f(x):
    if x <= p or x >= q:
        return abs(2**x - 4)
    else:
        return a + np.log2(x)

# 1) Check f((p+q)/2) == 2
mid = (p + q) / 2  # 1.5
val = f(mid)
assert abs(val - 2) < 1e-9, f'f(3/2) = {val}, expected 2'

# 2) Verify three ranges partition R (sample checks)
# Left outer piece range should be [3, 4)
left_samples = np.linspace(-50, 0, 10000)
left_vals = np.array([f(x) for x in left_samples])
assert left_vals.min() >= 3 - 1e-9, 'left range below 3'
assert left_vals.max() < 4, 'left range reaches 4'

# Middle piece range should be (-inf, 3)
mid_samples = np.linspace(1e-9, 3 - 1e-9, 10000)
mid_vals = np.array([f(x) for x in mid_samples])
assert mid_vals.max() < 3, 'middle range reaches 3'

# Right outer piece range should be [4, inf)
right_samples = np.linspace(3, 50, 10000)
right_vals = np.array([f(x) for x in right_samples])
assert right_vals.min() >= 4 - 1e-9, 'right range below 4'

# 3) Injectivity: each piece must be strictly monotone
assert np.all(np.diff(left_vals) <= 0), 'left piece not monotone decreasing'
assert np.all(np.diff(mid_vals) >= 0), 'middle piece not monotone increasing'
assert np.all(np.diff(right_vals) >= 0), 'right piece not monotone increasing'

print('VERIFY_PASS')
