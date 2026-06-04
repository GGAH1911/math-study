import math
cos_theta = 1 / math.sqrt(10)
sin_theta = -3 / math.sqrt(10)
tan_theta = sin_theta / cos_theta
assert abs(cos_theta**2 - 1/10) < 1e-10, f'cos^2 check failed: {cos_theta**2}'
assert abs(sin_theta**2 + cos_theta**2 - 1) < 1e-10, f'identity check failed'
assert abs(tan_theta - (-3)) < 1e-10, f'tan value check failed: {tan_theta}'
assert 3*math.pi/2 < math.atan2(sin_theta, cos_theta) + 2*math.pi < 2*math.pi or math.atan2(sin_theta, cos_theta) < 0, f'quadrant check'
print('VERIFY_PASS')