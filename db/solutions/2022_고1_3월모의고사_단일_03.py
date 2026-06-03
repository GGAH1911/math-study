import math
angle_60 = math.radians(60)
angle_30 = math.radians(30)
result = math.sin(angle_60) * math.cos(angle_30)
expected = 3/4
if abs(result - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')