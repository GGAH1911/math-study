import math
from sympy import sqrt, simplify

a = -15/4
r = 25/4

sin_theta = a / r
cos_theta = 5 / r

result = sin_theta + 2 * cos_theta
identity = sin_theta**2 + cos_theta**2

if abs(result - 1.0) < 1e-10 and abs(identity - 1.0) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')