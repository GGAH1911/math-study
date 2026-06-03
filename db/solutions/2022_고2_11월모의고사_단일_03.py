import math

# 원래 식 계산
result = math.log(12, 81) - math.log(4, 81)

# 답: 1/4
answer = 1/4

# 검증: 두 값이 같은지 확인
if abs(result - answer) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')