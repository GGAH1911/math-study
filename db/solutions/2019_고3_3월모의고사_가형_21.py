import numpy as np
from scipy.integrate import quad

# Define f'(x) and f(x)
def f_prime(x):
    return x * np.exp(-x**2)

def f(x):
    return 0.5 * (np.exp(-1) - np.exp(-x**2))

# Verify f'(x) by numerical differentiation
x_test = 1.0
epsilon = 1e-8
f_prime_check = (f(x_test + epsilon) - f(x_test - epsilon)) / (2 * epsilon)
f_prime_analytical = f_prime(x_test)
assert abs(f_prime_check - f_prime_analytical) < 1e-5, f'f prime mismatch'

# Check f(1) = 0
assert abs(f(1)) < 1e-10, 'f(1) should be 0'

# Define g(x) via numerical integration
def g(x):
    if x <= 1:
        def integrand(t):
            return f_prime(t) * (x + 1 - t)
        result, _ = quad(integrand, 1, x)
        return result
    else:
        def integrand(t):
            return f_prime(t) * (x + 1 - t)
        result, _ = quad(integrand, 1, x)
        return result

# Check g(1) = 0
assert abs(g(1)) < 1e-6, 'g(1) should be 0'

# Verify ㄱ: g'(1) = 1/e
epsilon = 1e-7
g_prime_1 = (g(1 + epsilon) - g(1 - epsilon)) / (2 * epsilon)
expected_1_e = 1 / np.e
assert abs(g_prime_1 - expected_1_e) < 1e-4, f'g\'(1) = {g_prime_1}, expected {expected_1_e}'

# Verify ㄴ: f(1) = g(1)
assert abs(f(1) - g(1)) < 1e-6, 'f(1) should equal g(1)'

# Verify ㄷ: check if g(x) < f(x) for some positive x
h_max = float('-inf')
for x_val in np.linspace(0.1, 3, 100):
    h_val = g(x_val) - f(x_val)
    h_max = max(h_max, -h_val)  # Track minimum of h

# If h(x) >= 0 for all tested x, then ㄷ is false
if h_max < 1e-5:
    result = 'VERIFY_PASS'
else:
    result = 'VERIFY_FAIL'

print(result)