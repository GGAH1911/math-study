import math
log_517_actual = math.log10(517)
table_log_5_17 = 0.7135
answer = table_log_5_17 + 2
if abs(answer - log_517_actual) < 0.0005:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')