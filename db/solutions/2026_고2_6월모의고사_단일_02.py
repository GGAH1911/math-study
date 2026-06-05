import math

# 원래 문제식
result = math.log(3/2, 3) + math.log(6, 3)

# 정답이 2인지 확인
if abs(result - 2) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')