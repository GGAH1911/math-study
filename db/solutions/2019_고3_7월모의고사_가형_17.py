from sympy import *
theta = symbols('theta', real=True, positive=True)
S = sin(theta) * (1 - cos(theta))
limit_val = limit(S / theta**3, theta, 0, '+')
if limit_val == Rational(1, 2):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')