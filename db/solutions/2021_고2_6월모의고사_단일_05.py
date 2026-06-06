import math
result = math.log10(3.14 * 10**(-2))
expected = -1.5031
if abs(result - expected) < 0.00005:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')