import math
a = 1/4
log_a_2 = math.log(2) / math.log(a)
log_a_4 = math.log(4) / math.log(a)
slope = (log_a_4 - log_a_2) / (4 - 2)
expected_slope = -1/4
if abs(slope - expected_slope) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')