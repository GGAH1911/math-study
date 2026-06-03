import math

# 지수 계산
exponent = (1 - math.sqrt(5)) + (1 + math.sqrt(5))
result = 3**exponent

# 검증: 답이 9인지 확인
if abs(result - 9) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')