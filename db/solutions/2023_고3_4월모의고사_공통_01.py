import math
result = math.log(4, 6) + 2 / math.log(6, 3)
print('VERIFY_PASS' if abs(result - 2.0) < 1e-10 else 'VERIFY_FAIL')