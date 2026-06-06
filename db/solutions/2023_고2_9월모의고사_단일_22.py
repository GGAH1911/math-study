import math

# 원래 문제식
result = math.log2(8) + math.log2(1/2)

# 검증: 결과가 2인지 확인
answer = 2
if abs(result - answer) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')