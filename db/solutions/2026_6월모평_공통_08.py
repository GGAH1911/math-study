import sympy as sp
from sympy import sin, cos, pi, sqrt, symbols, Eq, solve

theta = symbols('theta', real=True)
cos_theta_val = sqrt(5)/5

# Original conditions
# 1. sin(pi - theta) > 0 which is sin(theta) > 0
# 2. 2*cos(theta) = sin(theta)

# Verify condition 2: 2*cos(theta) = sin(theta)
sin_theta_computed = 2 * cos_theta_val
sin_theta_from_identity = sqrt(1 - cos_theta_val**2)

# sin(theta) should be positive
sin_theta = sin_theta_from_identity  # positive root

# Check: 2*cos(theta) should equal sin(theta)
lhs = 2 * cos_theta_val
rhs = sin_theta

if abs(float(lhs - rhs)) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')