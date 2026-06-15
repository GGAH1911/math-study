from sympy import *
a = symbols('a', real=True, positive=True)
cos_a = Rational(1, 3)
sin_a = sqrt(1 - cos_a**2)
A2 = 1 - cos_a
A1 = sin_a**2 / (2*cos_a) + cos_a - 1
if simplify(A1 - A2) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')