import math
from math import sqrt

# Given values
mag_a = sqrt(11)
mag_b = 3
mag_2a_minus_b = sqrt(17)

# Find a·b from |2a - b|² = 17
# 4|a|² - 4(a·b) + |b|² = 17
# 4(11) - 4(a·b) + 9 = 17
# 44 - 4(a·b) + 9 = 17
# a·b = (44 + 9 - 17) / 4 = 36/4 = 9
a_dot_b = (4 * 11 + 9 - 17) / 4

# Verify the constraint
verify_constraint = 4 * 11 - 4 * a_dot_b + 9
assert abs(verify_constraint - 17) < 1e-9, f'Constraint check failed: {verify_constraint}'

# Calculate |a - b|²
mag_a_minus_b_squared = mag_a**2 - 2 * a_dot_b + mag_b**2
mag_a_minus_b = sqrt(mag_a_minus_b_squared)

# Expected answer is sqrt(2)
expected = sqrt(2)
assert abs(mag_a_minus_b - expected) < 1e-9, f'Answer mismatch: {mag_a_minus_b} vs {expected}'

print('VERIFY_PASS')