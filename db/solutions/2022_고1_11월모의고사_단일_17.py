import numpy as np

def f(x):
    return x - 3

def g(x):
    return f(x) * f(abs(x - 2))

# Check over dense grid
xs = np.linspace(-1, 5, 100000)
vals = np.array([g(xi) for xi in xs])

max_val = np.max(vals)
min_val = np.min(vals)
total = max_val + min_val

# Verify exact values
assert abs(max_val - 4.0) < 1e-4, f'max mismatch: {max_val}'
assert abs(min_val - (-1.0)) < 1e-4, f'min mismatch: {min_val}'
assert abs(total - 3.0) < 1e-4, f'sum mismatch: {total}'
print('VERIFY_PASS')
