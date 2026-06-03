import math
result = -math.cos(math.pi) - (-math.cos(-math.pi/2))
print('VERIFY_PASS' if abs(result - 1) < 1e-9 else 'VERIFY_FAIL')