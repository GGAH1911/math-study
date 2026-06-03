import math

cos_theta = math.sqrt(6) / 3
# theta in (3pi/2, 2pi) -> fourth quadrant, sin < 0
sin_sq = 1 - cos_theta**2
sin_theta = -math.sqrt(sin_sq)
tan_theta = sin_theta / cos_theta

expected = -math.sqrt(2) / 2

if abs(tan_theta - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
