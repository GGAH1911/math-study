import math
angle = (5/3) * math.pi
cos_value = math.cos(angle)
result = 10 * cos_value
if abs(result - 5) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')