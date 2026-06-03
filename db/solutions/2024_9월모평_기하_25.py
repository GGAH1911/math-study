import math
from math import sqrt, pi

# A(4, 3)에 대한 OA의 거리
OA_distance = sqrt(4**2 + 3**2)
assert OA_distance == 5, f'OA distance should be 5, got {OA_distance}'

# P가 나타내는 도형: 원점 중심, 반지름 5인 원
radius = OA_distance

# 원의 둘레
circumference = 2 * pi * radius

# 답: 10π
expected_answer = 10 * pi

if abs(circumference - expected_answer) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')