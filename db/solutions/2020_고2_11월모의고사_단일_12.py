import sympy as sp
cos_theta = sp.Rational(1, 4)
sin_pi_2_plus_theta = cos_theta
cos_pi_minus_theta = -cos_theta
result = 3 * sin_pi_2_plus_theta + cos_pi_minus_theta
if result == sp.Rational(1, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')