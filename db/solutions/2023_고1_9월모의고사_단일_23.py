import math

# 부등식 |x-5| < 2를 만족하는 정수들
integers = []
for x in range(-100, 101):
    if abs(x - 5) < 2:
        integers.append(x)

# 답: 모든 정수의 합
answer_sum = sum(integers)
expected = 15

if answer_sum == expected:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')