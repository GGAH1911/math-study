import math
from fractions import Fraction

# 부채꼴 넓이 공식: A = (1/2) * r^2 * theta
r = 2
theta = math.pi / 6
A_calculated = 0.5 * r**2 * theta
A_expected = math.pi / 3

if abs(A_calculated - A_expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')