import math
answer = 1.3892
actual = math.log10(24.5)
if abs(answer - actual) < 0.0001:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')