import sympy as sp
theta = sp.Symbol('theta')
cos_theta = -3/5
sin_theta = 4/5
verify_cos = -cos_theta
verify_tan = sin_theta / cos_theta
assert abs(verify_cos - 3/5) < 1e-10, f'cos(theta-pi) check failed: {verify_cos}'
assert verify_tan < 0, f'tan(theta) < 0 check failed: {verify_tan}'
assert abs(sin_theta**2 + cos_theta**2 - 1) < 1e-10, 'Pythagorean identity failed'
print('VERIFY_PASS')