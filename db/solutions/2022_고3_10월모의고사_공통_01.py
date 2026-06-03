import math
result = math.sqrt(8) * (4 ** 0.25)
print('VERIFY_PASS' if abs(result - 4.0) < 1e-9 else 'VERIFY_FAIL')