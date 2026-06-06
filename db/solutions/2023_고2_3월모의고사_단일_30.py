import numpy as np
from scipy.optimize import fsolve

# Case 1: a=-2, b=-1
a, b = -2, -1

def f1(x):
    if x <= -2:
        return (1 - a) / (x - 1) + 2
    else:
        return b * x * (x - a) + 1

# f(x) = 2 solutions for x > -2
# -x(x+2) = 1 => x^2 + 2x + 1 = 0
roots_2_case1 = [-1]
count_2_case1 = sum(1 for r in roots_2_case1 if r > -2)

# f(x) = -2 solutions for x > -2
# -x(x+2) = -3 => x^2 + 2x - 3 = 0 => (x-1)(x+3) = 0
roots_neg2_case1_all = [1, -3]
count_neg2_case1 = sum(1 for r in roots_neg2_case1_all if r > -2)

total_1 = count_2_case1 + count_neg2_case1

# Case 2: a=-4, b=3/4
a, b = -4, 0.75

# f(x) = -2 for x > -4: (3/4)x(x+4) = -3 => x^2 + 4x + 4 = 0
discriminant = 16 - 16
if discriminant >= 0:
    root_neg2_case2 = -2
    count_neg2_case2 = 1 if root_neg2_case2 > -4 else 0
else:
    count_neg2_case2 = 0

# f(x) = 2 for x > -4: (3/4)x(x+4) = 1 => 3x^2 + 12x - 4 = 0
import math
discriminant_2 = 144 + 48
if discriminant_2 > 0:
    sqrt_val = math.sqrt(discriminant_2)
    r1 = (-12 + sqrt_val) / 6
    r2 = (-12 - sqrt_val) / 6
    count_2_case2 = sum(1 for r in [r1, r2] if r > -4)
else:
    count_2_case2 = 0

total_2 = count_2_case2 + count_neg2_case2

if total_1 == 2 and total_2 == 2:
    result = -40 * ((-2) + (-1) + (-4) + 0.75)
    print('VERIFY_PASS') if abs(result - 250) < 0.01 else print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')