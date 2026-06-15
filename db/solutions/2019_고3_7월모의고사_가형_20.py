from scipy.integrate import quad
import numpy as np

def f(x):
    return 3/2 - 2*np.cos(np.pi*x)

def f_prime(x):
    return 2*np.pi*np.sin(np.pi*x)

# Check ㄱ: f(x+2) = f(x)
x_test = 0.5
assert abs(f(x_test + 2) - f(x_test)) < 1e-10, 'ㄱ failed'

# Check ㄴ: f(1) - f(0) = 4
assert abs(f(1) - f(0) - 4) < 1e-10, 'ㄴ failed'

# Check ∫₂⁵f'(x)dx = 4
int_f_prime, _ = quad(f_prime, 2, 5)
assert abs(int_f_prime - 4) < 1e-10, 'condition failed'

# Check ∫₀¹f(f(x))f'(x)dx = 6
def integrand(x):
    return f(f(x)) * f_prime(x)
int_condition, _ = quad(integrand, 0, 1)
assert abs(int_condition - 6) < 1e-10, 'ㄷ condition failed'

# Check ∫₁¹⁰f(x)dx = 27/2
int_result, _ = quad(f, 1, 10)
expected = 27/2
assert abs(int_result - expected) < 1e-10, f'ㄷ failed: {int_result} != {expected}'

print('VERIFY_PASS')