import sympy as sp
from sympy import cos, sin, pi, sqrt

# theta in third quadrant (π < θ < 3π/2)
# verify that sin(theta) = -1/3 satisfies the equation

sin_theta = -1/3
cos_theta_sq = 1 - sin_theta**2
cos_theta_sq_val = float(cos_theta_sq)

# In third quadrant, cos(theta) < 0
cos_theta = -sqrt(cos_theta_sq_val)

# Verify the original equation: 1/(1-cos(theta)) + 1/(1+cos(theta)) = 18
lhs = 1/(1 - float(cos_theta)) + 1/(1 + float(cos_theta))

if abs(lhs - 18) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')