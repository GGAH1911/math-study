import sympy as sp
import numpy as np
from scipy.integrate import quad

# 역대입 검증
def f_0_1(x):
    return -x**2 + 4*x - 2

def f_1_5(x):
    return np.exp(2*np.sqrt(x-1)) - 2*np.sqrt(x-1)

# 조건 (가) 검증: x < 1일 때 f'(x) = -2x + 4
f_prime_0_1 = lambda x: -2*x + 4
f_deriv_computed_0_1 = lambda x: -2*x + 4  # f(x) = -x^2 + 4x - 2 미분
assert np.allclose(f_deriv_computed_0_1(0.5), f_prime_0_1(0.5)), 'Condition (가) failed'

# 조건 (나) 검증: x >= 0에 대해 f(x^2+1) = e^(2x) - 2x
for x_test in [0, 0.5, 1, 1.5, 2]:
    x_sq_plus_1 = x_test**2 + 1
    if x_sq_plus_1 < 1:
        f_val = f_0_1(x_sq_plus_1)
    else:
        f_val = f_1_5(x_sq_plus_1)
    expected = np.exp(2*x_test) - 2*x_test
    assert np.allclose(f_val, expected, atol=1e-10), f'Condition (나) failed at x={x_test}'

# 적분 검증
result_0_1, _ = quad(f_0_1, 0, 1)
result_1_5, _ = quad(f_1_5, 1, 5)
total = result_0_1 + result_1_5

expected_integral = 1.5 * np.exp(4) - 10.5
assert np.allclose(total, expected_integral, atol=1e-10), f'Integral mismatch: {total} vs {expected_integral}'

print('VERIFY_PASS')