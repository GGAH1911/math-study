from sympy import symbols, solve, sqrt

CANDIDATE = 3

def f(n_value):
    """f(n) = (n-3)^2 + 2"""
    return (n_value - 3) ** 2 + 2

# h(0): 1 < f(n) < 9
# (n-3)^2 + 2 < 9 => (n-3)^2 < 7
# => 3 - sqrt(7) < n < 3 + sqrt(7)
# => approximately 0.354 < n < 5.646
# Natural numbers: {1, 2, 3, 4, 5}
h_0_count = sum(1 for n in range(1, 20) if 1 < f(n) < 9)

# h(3): 27 < f(n) < 243
# (n-3)^2 + 2 > 27 => (n-3)^2 > 25 => |n-3| > 5
# For natural numbers: n >= 9
# (n-3)^2 + 2 < 243 => (n-3)^2 < 241 => |n-3| < sqrt(241) ≈ 15.524
# For natural numbers: n <= 18
# Range: {9, 10, ..., 18}
h_3_count = sum(1 for n in range(1, 30) if 27 < f(n) < 243)

# Compute sum h(0) + h(3)
computed_sum = h_0_count + h_3_count

# Map option number to answer value
options = {1: 11, 2: 13, 3: 15, 4: 17, 5: 19}
expected_value = options[CANDIDATE]

# Verification: core relation is h(0) + h(3) = option_value
if computed_sum == expected_value:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: h(0)={h_0_count}, h(3)={h_3_count}, computed_sum={computed_sum}, expected_option_{CANDIDATE}={expected_value}')