import math
answer = 3
result = math.log(54, 3) - math.log(2, 3)
if abs(result - answer) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')