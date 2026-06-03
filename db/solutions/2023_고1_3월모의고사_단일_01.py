import math
result = math.sqrt(12/5) * math.sqrt(5/3)
if abs(result - 2) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')