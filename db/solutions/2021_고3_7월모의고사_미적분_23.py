import sympy as sp
sin_theta = sp.sqrt(5) / 5
sin_squared = sin_theta**2
cos_squared = 1 - sin_squared
cos_theta = sp.sqrt(cos_squared)
sec_theta = 1 / cos_theta
sec_theta_simplified = sp.simplify(sec_theta)
expected = sp.sqrt(5) / 2
if sp.simplify(sec_theta_simplified - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')