import math
result = 2 * (16 ** 0.5)
if abs(result - 8) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')