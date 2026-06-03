import math

# 주어진 값
r = 4
theta = 5 * math.pi / 12

# 부채꼴 넓이 공식
area = 0.5 * r**2 * theta

# 정답 (π 계수)
answer_coefficient = area / math.pi
expected_coefficient = 10 / 3

# 검증
if abs(answer_coefficient - expected_coefficient) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')