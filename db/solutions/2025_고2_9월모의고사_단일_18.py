import numpy as np

a = 4
b = 1

x_vals = np.linspace(0, np.pi, 1000000)
f_vals = a * np.cos(b * x_vals - np.pi / 4)

max_f = np.max(f_vals)
min_f = np.min(f_vals)

expected_max = 4.0
expected_min = -2 * np.sqrt(2)

if abs(max_f - expected_max) < 1e-5 and abs(min_f - expected_min) < 1e-5:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: max={max_f:.8f} (expected {expected_max}), min={min_f:.8f} (expected {expected_min:.8f})')