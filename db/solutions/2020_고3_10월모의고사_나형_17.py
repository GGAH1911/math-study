from sympy import symbols, diff, limit, solve, Function

# f(1) = -2, g(x) = x + 1 (from conditions)
# Check: g(0) = 1, g'(0) = 1 ✓

# From condition (가): lim_{x→1} [f(x)(x+1)+4]/(x-1) = 8
# Since f(1)*g(1)+4 = 0 (numerator approaches 0), use L'Hôpital
# Result: f'(1)*2 + f(1) = 8
# f'(1)*2 + (-2) = 8
# f'(1) = 5

f_prime_1 = 5

# Verification
g_at_0 = 1  # x + 1 evaluated at 0
g_prime_at_0 = 1  # derivative of x+1
assert g_at_0 == g_prime_at_0, "Condition (나) failed"

f_at_1 = -2
g_at_1 = 2
f_times_g_plus_4 = f_at_1 * g_at_1 + 4
assert f_times_g_plus_4 == 0, "Numerator not zero at x=1"

# L'Hôpital result
limit_value = f_prime_1 * 2 + f_at_1
assert limit_value == 8, f"Limit should be 8, got {limit_value}"

print('VERIFY_PASS')