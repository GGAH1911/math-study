import numpy as np

# Original function: f(x) = -sin(2x) on [0, pi]
def f(x):
    return -np.sin(2 * x)

# Find maximum and minimum by scanning
xs = np.linspace(0, np.pi, 100000)
ys = f(xs)

a = xs[np.argmax(ys)]  # x where f has maximum
b = xs[np.argmin(ys)]  # x where f has minimum

fa = f(a)
fb = f(b)

# Expected: a ≈ 3pi/4, fa ≈ 1; b ≈ pi/4, fb ≈ -1
a_exact = 3 * np.pi / 4
b_exact = np.pi / 4

assert abs(a - a_exact) < 1e-3, f'a mismatch: {a} vs {a_exact}'
assert abs(b - b_exact) < 1e-3, f'b mismatch: {b} vs {b_exact}'
assert abs(fa - 1.0) < 1e-6, f'f(a) mismatch: {fa}'
assert abs(fb - (-1.0)) < 1e-6, f'f(b) mismatch: {fb}'

# Slope of line through (a, f(a)) and (b, f(b))
slope = (fa - fb) / (a_exact - b_exact)
expected_slope = 4 / np.pi

if abs(slope - expected_slope) < 1e-9:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: slope={slope}, expected={expected_slope}')
