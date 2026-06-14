import sympy as sp
cos_theta = sp.Rational(-3, 5)
sin_squared = 1 - cos_theta**2
sin_theta = -sp.sqrt(sin_squared)
tan_theta = sp.simplify(sin_theta / cos_theta)
expected = sp.Rational(4, 3)
if tan_theta == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')