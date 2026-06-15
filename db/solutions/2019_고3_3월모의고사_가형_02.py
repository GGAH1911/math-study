from sympy import Rational, sec, acos
cos_theta = Rational(2, 3)
theta = acos(cos_theta)
sec_val = sec(theta)
expected = Rational(3, 2)
if sec_val == expected and (1/cos_theta) == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')