import math

cos_theta = -3/4
sin_squared = 1 - cos_theta**2
sin_theta = math.sqrt(sin_squared)

theta = math.acos(cos_theta)

if math.pi/2 < theta < math.pi and abs(sin_theta - math.sqrt(7)/4) < 1e-10:
    identity_check = sin_theta**2 + cos_theta**2
    if abs(identity_check - 1) < 1e-10:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')