import math
result = math.log2(48) - math.log2(3)
expected = 4
if abs(result - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')