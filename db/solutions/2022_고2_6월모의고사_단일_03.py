import math

r = 6
arc_length = 4 * math.pi
theta = 2 * math.pi / 3

computed_arc = r * theta

if abs(computed_arc - arc_length) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')