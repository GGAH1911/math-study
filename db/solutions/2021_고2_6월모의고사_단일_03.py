import math
r = 6
area_given = 15 * math.pi
theta = 5 * math.pi / 6
calculated_area = 0.5 * r**2 * theta
if abs(calculated_area - area_given) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')