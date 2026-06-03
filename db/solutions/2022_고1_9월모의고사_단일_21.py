import numpy as np
A, B, C = np.array([-5, 0]), np.array([0, -5]), np.array([4, 3])
sin_theta = 3 / np.sqrt(10)
cos_theta = -1 / np.sqrt(10)
P = np.array([5 * cos_theta, 5 * sin_theta])
dist_B_AC = abs(0 - 3*(-5) + 5) / np.sqrt(10)
expected_dist = 2 * np.sqrt(10)
verts = [A, P, C, B]
area = abs(sum(verts[i][0]*verts[(i+1)%4][1] - verts[(i+1)%4][0]*verts[i][1] for i in range(4))) / 2
expected_area = 15 * (3 + np.sqrt(10)) / 2
PB = B - P
AC = C - A
dot = np.dot(PB, AC)
assert np.isclose(dist_B_AC, expected_dist)
assert np.isclose(area, expected_area)
assert not np.isclose(dot, 0)
print('VERIFY_PASS')