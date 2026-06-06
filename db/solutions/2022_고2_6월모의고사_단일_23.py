import math
x = 24
result = math.log(x + 1, 5)
if abs(result - 2.0) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')