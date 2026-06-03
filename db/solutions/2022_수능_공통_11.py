import math
from math import tan, pi, sqrt

# a = 4√3/3
a = 4*sqrt(3)/3

# t = -π/4, so x_A = -√3/3
x_A = -sqrt(3)/3
f_x_A = tan(pi*x_A/a)
expected_f_A = sqrt(3)*x_A

# x_B = √3/3
x_B = sqrt(3)/3
f_x_B = tan(pi*x_B/a)
expected_f_B = sqrt(3)*x_B

# C coordinates
x_C = x_A + a
f_x_C = f_x_A  # same y-coordinate as A

# Verify A, B are on the line y = √3·x through O
slope_OA = f_x_A / x_A if x_A != 0 else float('inf')
slope_OB = f_x_B / x_B if x_B != 0 else float('inf')

# Verify equilateral triangle
dist_AC = abs(x_C - x_A)
dist_AB = sqrt((x_B - x_A)**2 + (f_x_B - f_x_A)**2)
dist_BC = sqrt((x_C - x_B)**2 + (f_x_C - f_x_B)**2)

# Area calculation
area = sqrt(3)/4 * a**2
expected_area = 4*sqrt(3)/3

# Checks
check1 = abs(f_x_A - expected_f_A) < 1e-10
check2 = abs(f_x_B - expected_f_B) < 1e-10
check3 = abs(slope_OA - sqrt(3)) < 1e-10
check4 = abs(slope_OB - sqrt(3)) < 1e-10
check5 = abs(dist_AC - a) < 1e-10
check6 = abs(dist_AB - a) < 1e-10
check7 = abs(dist_BC - a) < 1e-10
check8 = abs(area - expected_area) < 1e-10

if all([check1, check2, check3, check4, check5, check6, check7, check8]):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')