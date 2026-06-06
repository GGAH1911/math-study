import numpy as np

# 부등식 |x-2| < 3 을 만족하는 정수 개수
# -1 < x < 5 를 만족하는 정수를 구함

integers_in_range = [x for x in range(-10, 10) if abs(x - 2) < 3]
count = len(integers_in_range)

if count == 5 and integers_in_range == [0, 1, 2, 3, 4]:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')