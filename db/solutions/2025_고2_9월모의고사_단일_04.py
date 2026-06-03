import sympy as sp
cos_theta = sp.Rational(1, 3)
sin_squared = 1 - cos_theta**2
sin_theta = -sp.sqrt(sin_squared)
tan_theta = sin_theta / cos_theta
expected = -2*sp.sqrt(2)
if sp.simplify(tan_theta - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')