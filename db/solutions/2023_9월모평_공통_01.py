import math
sqrt_3 = math.sqrt(3)
base = 2**(sqrt_3 - 1)
exponent = sqrt_3 + 1
result = base ** exponent
expected = 4
if abs(result - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')