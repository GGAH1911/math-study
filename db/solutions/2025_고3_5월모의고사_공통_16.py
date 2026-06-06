import math
x = 10
left = math.log(x - 3) / math.log(3**0.5)
right = math.log(5*x - 1) / math.log(3)
if abs(left - right) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')