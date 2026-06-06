import math
log3_7 = math.log(7) / math.log(3)
log7_9 = math.log(9) / math.log(7)
result = log3_7 * log7_9
if abs(result - 2.0) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')