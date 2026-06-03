import math
x1, y1 = 1, 3
x2, y2 = 2, 5
dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
expected = math.sqrt(5)
if abs(dist - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')