import math
x = 2
left = math.log(x+1, 5) + math.log(x-1, 5)
right = math.log(9, 25)
if abs(left - right) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')