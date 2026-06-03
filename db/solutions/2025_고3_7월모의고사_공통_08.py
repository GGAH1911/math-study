import math
a, b = 2, 4
result = math.log(a, 2) + math.log(a * b, 4)
expected = 2.5
if abs(result - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')