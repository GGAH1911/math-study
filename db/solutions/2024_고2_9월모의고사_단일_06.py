import math

# 원래 식: log_2(5) * log_5(3) + log_2(16/3)
log2_5 = math.log(5) / math.log(2)
log5_3 = math.log(3) / math.log(5)
log2_16_3 = math.log(16/3) / math.log(2)

result = log2_5 * log5_3 + log2_16_3

if abs(result - 4) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')