import math
result = math.tan(10*math.pi/3)
expected = math.sqrt(3)
if abs(result - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')