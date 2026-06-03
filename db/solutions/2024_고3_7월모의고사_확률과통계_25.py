from fractions import Fraction
a_plus_b = Fraction(2, 3)
a2_plus_b2 = Fraction(5, 18)
ab = Fraction(1, 12)

# Check: (a+b)^2 = a^2 + 2ab + b^2
lhs = a_plus_b**2
rhs = a2_plus_b2 + 2*ab
assert lhs == rhs, f'Square identity failed: {lhs} != {rhs}'

# Verify discriminant and roots
import math
discriminant = a_plus_b**2 - 4*ab
assert discriminant == Fraction(1, 9)
root_d = Fraction(1, 3)
a_val = (a_plus_b - root_d) / 2
b_val = (a_plus_b + root_d) / 2
assert a_val == Fraction(1, 6)
assert b_val == Fraction(1, 2)

# Verify conditions
assert a_val + b_val == Fraction(2, 3)
assert a_val**2 + b_val**2 == Fraction(5, 18)
assert a_val * b_val == Fraction(1, 12)
assert 0 < a_val < b_val

# Verify probability distribution
P_0 = Fraction(1, 3)
P_a = a_val
P_b = b_val
assert P_0 + P_a + P_b == 1
assert all(0 <= p <= 1 for p in [P_0, P_a, P_b])

# Verify expectation
E_X = 0 * P_0 + a_val * P_a + b_val * P_b
assert E_X == Fraction(5, 18)

print('VERIFY_PASS')