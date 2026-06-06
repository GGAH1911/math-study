import numpy as np
from math import sqrt, pi

# Given values
cos_theta = 3/8
sin_theta = sqrt(55)/8

# Coordinates
A = np.array([9/8, 3*sqrt(55)/8])
B = np.array([0, 0])
C = np.array([4, 0])

# Verify AB=3, AC=4
AB = np.linalg.norm(A - B)
AC = np.linalg.norm(A - C)
assert abs(AB - 3) < 1e-10
assert abs(AC - 4) < 1e-10

# External circle condition
Area_ABC = pi * (25 - 24*cos_theta) / (4 * sin_theta**2)
Area_ADE = pi * cos_theta**2 * (25 - 24*cos_theta) / (4 * sin_theta**2)
diff = Area_ABC - Area_ADE
assert abs(diff - 4*pi) < 1e-9

# P = (9/8, 69*sqrt(55)/440)
P = np.array([9/8, 69*sqrt(55)/440])

# Check |AP|
AP_dist_sq = (A[0] - P[0])**2 + (A[1] - P[1])**2
assert abs(AP_dist_sq - 144/55) < 1e-9

# Circumradius of triangle PDE
R_sq = AP_dist_sq / 4
Area_PDE_circle = pi * R_sq
expected_area = 36*pi/55
assert abs(Area_PDE_circle - expected_area) < 1e-9

a = 36/55
result = 55 * a
assert abs(result - 36) < 1e-9

print('VERIFY_PASS')