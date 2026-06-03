import math

# Given: cos(pi + theta) = 1/3, sin(pi + theta) > 0
# Derived: cos(theta) = -1/3, sin(theta) < 0

cos_theta = -1/3
# sin^2 + cos^2 = 1
sin_sq = 1 - cos_theta**2
sin_theta = -math.sqrt(sin_sq)  # negative because sin(theta) < 0

# Verify original conditions
cond1 = math.isclose(math.cos(math.pi) * cos_theta - math.sin(math.pi) * sin_theta, 1/3, rel_tol=1e-9)
# cos(pi+theta) = cos(pi)cos(theta) - sin(pi)sin(theta) = -cos(theta)
cond1 = math.isclose(-cos_theta, 1/3, rel_tol=1e-9)
cond2 = (-sin_theta) > 0  # sin(pi+theta) = -sin(theta) > 0

# Compute tan(theta)
tan_theta = sin_theta / cos_theta
expected = 2 * math.sqrt(2)
cond3 = math.isclose(tan_theta, expected, rel_tol=1e-9)

if cond1 and cond2 and cond3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print(f'cond1={cond1}, cond2={cond2}, cond3={cond3}, tan={tan_theta}, expected={expected}')
