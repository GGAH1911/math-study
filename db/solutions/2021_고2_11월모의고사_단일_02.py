import math

# 원래 식 검증
log3_18 = math.log(18) / math.log(3)
log3_2 = math.log(2) / math.log(3)
result = log3_18 - log3_2

# 우리 답이 2인지 확인
if abs(result - 2) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')