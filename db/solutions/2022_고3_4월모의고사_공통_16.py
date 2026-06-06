import math

# 원래 문제의 식을 계산
log2_9 = math.log(9) / math.log(2)
log3_16 = math.log(16) / math.log(3)
result = log2_9 * log3_16

# 답 검증
answer = 8
if abs(result - answer) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')