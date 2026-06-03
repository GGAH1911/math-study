import math

log_5_3 = math.log(3) / math.log(5)
log_5_4 = math.log(4) / math.log(5)
log_5_12 = math.log(12) / math.log(5)

m = (1 - log_5_3) / log_5_4

result = (1 - m) * log_5_3 + m * log_5_12

value_4_m = 4 ** m
expected = 5 / 3

if abs(result - 1.0) < 1e-9 and abs(value_4_m - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')