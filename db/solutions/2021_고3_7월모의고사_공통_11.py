import math
from math import log

# a^10 = 24이므로 a^20 = 576
a_to_20 = 576
a = a_to_20 ** (1/20)

# 검증: log_a(9) + 2*log_a(8) = 20인지 확인
log_a_9 = log(9) / log(a)
log_a_8 = log(8) / log(a)

result = log_a_9 + 2 * log_a_8

if abs(result - 20) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')