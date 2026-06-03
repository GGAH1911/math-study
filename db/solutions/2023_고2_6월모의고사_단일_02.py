import math

# 원래 문제 식 검증
log4_64 = math.log(64) / math.log(4)
log4_8 = math.log(8) / math.log(4)
result = log4_64 / log4_8

if abs(result - 2.0) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')