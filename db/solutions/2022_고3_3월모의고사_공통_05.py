from sympy import *
theta = 5*pi/6
sin_val = sin(theta)
cos_val = cos(theta)
tan_val = sin_val/cos_val
product = cos_val*tan_val
assert simplify(product - Rational(1,2)) == 0
result = cos_val + tan_val
expected = -5*sqrt(3)/6
if simplify(result - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')