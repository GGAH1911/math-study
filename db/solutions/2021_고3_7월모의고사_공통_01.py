import math
result = (4 ** 0.5) + math.log2(8)
print('VERIFY_PASS' if abs(result - 5) < 1e-10 else 'VERIFY_FAIL')