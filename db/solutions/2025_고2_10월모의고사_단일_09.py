import sympy as sp

theta = sp.Symbol('theta', real=True)
sin_val = sp.Rational(1, 2)

# cos^2 = 1 - sin^2
cos_sq = 1 - sin_val**2  # = 3/4

# 원래 식: 3*tan(pi+theta) = 2*sin(pi/2+theta)
# => 3*tan(theta) = 2*cos(theta)
# => 3*sin(theta) = 2*cos^2(theta)
LHS = 3 * sin_val
RHS = 2 * cos_sq

if LHS == RHS:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')