import math
result = math.sqrt(20/3) * math.sqrt(6/5)
expected = 2 * math.sqrt(2)
if abs(result - expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')