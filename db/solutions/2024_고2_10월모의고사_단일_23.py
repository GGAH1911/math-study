import math
r = 8
theta = 7 * math.pi / 8
arc_length = r * theta
area = 0.5 * r**2 * theta
expected_area = 28 * math.pi
expected_arc = 7 * math.pi
if abs(area - expected_area) < 1e-10 and abs(arc_length - expected_arc) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')