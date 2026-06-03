import math

# Step 1: Verify sigma from 95% CI with n=16
z_95 = 1.96
z_99 = 2.58
n1 = 16
ci_low = 746.1
ci_high = 755.9
width_given = ci_high - ci_low  # 9.8

# 2 * 1.96 * sigma / sqrt(16) = 9.8
sigma = width_given / (2 * z_95 / math.sqrt(n1))
assert abs(sigma - 10.0) < 1e-9, f'VERIFY_FAIL: sigma={sigma}'

# Step 2: Find minimum n such that 99% CI width <= 6
# b - a = 2 * 2.58 * 10 / sqrt(n) <= 6
n_answer = 74

b_minus_a_74 = 2 * z_99 * sigma / math.sqrt(n_answer)
b_minus_a_73 = 2 * z_99 * sigma / math.sqrt(73)

# n=74 must satisfy <= 6, n=73 must not
if b_minus_a_74 <= 6 and b_minus_a_73 > 6:
    print('VERIFY_PASS')
else:
    print(f'VERIFY_FAIL: b-a(74)={b_minus_a_74}, b-a(73)={b_minus_a_73}')
