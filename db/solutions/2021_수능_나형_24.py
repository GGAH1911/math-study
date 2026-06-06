import math

# 원래 문제의 식
original = math.log(72, 3) - math.log(8, 3)

# 우리의 답: 2
answer = 2

# 검증
if abs(original - answer) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')