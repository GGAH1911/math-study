import math
x = 27
result = math.log(x, 3)
if abs(result - 3.0) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')