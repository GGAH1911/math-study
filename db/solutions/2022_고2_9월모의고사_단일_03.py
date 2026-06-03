import math
angle = 4 * math.pi / 3
result = 12 * math.cos(angle)
if abs(result - (-6)) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')