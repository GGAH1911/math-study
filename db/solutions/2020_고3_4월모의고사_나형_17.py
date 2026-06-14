import numpy as np

r = 6
theta_CB = np.pi / 3

A = np.array([-6.0, 0.0])
B = np.array([6.0, 0.0])
C = np.array([r * np.cos(theta_CB), r * np.sin(theta_CB)])
O = np.array([0.0, 0.0])

AB = B - A
AC = C - A
area_ABC = 0.5 * abs(AB[0] * AC[1] - AB[1] * AC[0])

area_sector_OCB = 0.5 * r**2 * theta_CB

OC = C - O
OB = B - O
area_triangle_OCB = 0.5 * abs(OC[0] * OB[1] - OC[1] * OB[0])

area_segment = area_sector_OCB - area_triangle_OCB
total_area = area_ABC + area_segment

answer = 6 * np.pi + 9 * np.sqrt(3)

if np.isclose(total_area, answer):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')