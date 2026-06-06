import sympy as sp
cos_theta = sp.Rational(1, 3)
sin_squared = 1 - cos_theta**2
result = 9 * sin_squared
if result == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')