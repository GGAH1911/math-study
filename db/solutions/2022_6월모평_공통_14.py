import numpy as np
from numpy.polynomial import polynomial as P

p = 1
q = 7

def f(x):
    return x**3 - 3*x**2 - 9*x - 12

def h(x):
    return f(x - p) + q

# h(0) = 0 확인
assert abs(h(0)) < 1e-10, 'h(0) should be 0'

# h(x) = x^2(x-6) 확인
x_test = np.array([0.5, 1, 2, 6, 8])
h_expected = x_test**2 * (x_test - 6)
h_actual = h(x_test)
assert np.allclose(h_actual, h_expected), 'h(x) mismatch'

# h'(0) = 0 확인
h_prime_0 = 3*(p+3)*(p-1)
assert abs(h_prime_0) < 1e-10, 'h\'(0) should be 0'

# h'(6) ≠ 0 확인
h_prime_6 = 3*6*(6-4)
assert abs(h_prime_6 - 36) < 1e-10, 'h\'(6) should be 36'

print('VERIFY_PASS')