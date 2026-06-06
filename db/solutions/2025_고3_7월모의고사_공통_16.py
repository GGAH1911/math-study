import math
x = 2
left = 2 * math.log(x + 1) / math.log(3)
right = math.log(x + 7) / math.log(3)
if abs(left - right) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')