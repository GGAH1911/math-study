import numpy as np

# a = arctan(3)
a = np.arctan(3)

# Verify AP:BP = 1:3
AP = 2 * np.cos(a)
BP = 2 * np.sin(a)
assert abs(AP / BP - 1/3) < 1e-9, 'AP:BP ratio fail'

# f(theta) = (1 - cos2t)*sin2t
def f(theta):
    return (1 - np.cos(2*theta)) * np.sin(2*theta)

# Numerical derivative
h = 1e-8
f_prime_numerical = (f(a + h) - f(a - h)) / (2 * h)

# Analytical derivative: f'(theta) = 2cos2t - 2cos4t
cos2a = np.cos(2*a)
cos4a = np.cos(4*a)
f_prime_analytical = 2*cos2a - 2*cos4a

expected = -54/25

if abs(f_prime_analytical - expected) < 1e-6 and abs(f_prime_numerical - expected) < 1e-5:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: analytical={f_prime_analytical:.8f}, numerical={f_prime_numerical:.8f}, expected={expected:.8f}')
