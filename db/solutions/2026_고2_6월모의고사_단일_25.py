import math

# 원래 문제: log_3(2) * log_4(a) = 2
a = 81

# 밑 변환 공식으로 계산
log3_2 = math.log(2) / math.log(3)
log4_a = math.log(a) / math.log(4)

result = log3_2 * log4_a

if abs(result - 2.0) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')