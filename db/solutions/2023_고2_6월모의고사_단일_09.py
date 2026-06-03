import math
sin_theta = -1/3
cos_theta = -2*math.sqrt(2)/3
tan_theta = math.sqrt(2)/4
verified_sin = sin_theta
verified_tan = sin_theta / cos_theta
if abs(verified_tan - tan_theta) < 1e-10 and abs(sin_theta + 1/3) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')