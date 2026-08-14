import sympy as sp
from sympy import sin, cos, tan, sqrt, solve, Eq, atan

# Define k symbolically
k = sp.Symbol('k', real=True, positive=True)

# Given: tan k = 4/3
tan_k_value = sp.Rational(4, 3)

# From tan k = 4/3, we get sin k and cos k
# sin²k + cos²k = 1, and sin k / cos k = 4/3
# So sin k = 4/5, cos k = 3/5 (in first quadrant)
sin_k = sp.Rational(4, 5)
cos_k = sp.Rational(3, 5)

# Verify tan k
tan_k_check = sin_k / cos_k
assert tan_k_check == tan_k_value, f"tan k check failed: {tan_k_check} != {tan_k_value}"

# Compute a and b in terms of k
# a = cos k + k sin k = 3/5 + k * 4/5
# b = sin k - k cos k = 4/5 - k * 3/5

# For the angle condition, we already established tan k = 4/3
# Now verify the angle between tangent line and y = x/2
slope_tangent = tan_k_value  # 4/3
slope_reference = sp.Rational(1, 2)  # y = x/2

tan_theta = abs((slope_tangent - slope_reference) / (1 + slope_tangent * slope_reference))
assert tan_theta == sp.Rational(1, 2), f"Angle check failed: {tan_theta} != 1/2"

# Now compute 3a + 4b + tan k
# Since a = (3 + 4k)/5 and b = (4 - 3k)/5
# 3a + 4b = 3(3+4k)/5 + 4(4-3k)/5 = (9+12k+16-12k)/5 = 25/5 = 5

result = 5 + tan_k_value
candidate = sp.Rational(19, 3)

assert result == candidate, f"Final answer check failed: {result} != {candidate}"

print('VERIFY_PASS')