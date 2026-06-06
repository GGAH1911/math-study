import math

# 원래 문제의 식 검증
log2_96 = math.log(96) / math.log(2)
log_frac14_9 = math.log(9) / math.log(1/4)

result = log2_96 + log_frac14_9
answer = 5

if abs(result - answer) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')