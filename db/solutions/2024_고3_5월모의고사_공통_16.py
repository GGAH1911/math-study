import math
x = 5
left = math.log2(x - 3)
right = 1 - math.log2(x - 4)
if abs(left - right) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')