import math

# 원래 문제의 식을 검증
result = math.log(40, 5) + math.log(5/8, 5)

# 우리의 답이 맞는지 확인
answer = 2

if abs(result - answer) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')