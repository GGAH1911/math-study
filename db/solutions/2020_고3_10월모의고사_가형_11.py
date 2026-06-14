import math
from sympy import *

CANDIDATE = 5*pi/3

x_values = [2*pi/3, pi]
total = 0

for x_val in x_values:
    sin_x = sin(x_val)
    rhs = sqrt(3) * (1 + cos(x_val))
    total += x_val
    assert simplify(sin_x - rhs) == 0, f'Solution x={x_val} does not satisfy the equation'

verification_sum = total

if simplify(verification_sum - CANDIDATE) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')