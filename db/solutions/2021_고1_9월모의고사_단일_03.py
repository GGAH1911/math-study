import math

# 두 점의 좌표
P = (1, 2)
Q = (-2, 1)

# 거리 계산
distance = math.sqrt((Q[0] - P[0])**2 + (Q[1] - P[1])**2)

# √10의 값
answer_value = math.sqrt(10)

# 검증
if abs(distance - answer_value) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')