import math

# 주어진 조건: 호의 길이 = 원의 둘레의 1/5
# 반지름 r에 대해
r = 1  # 임의의 반지름
circumference = 2 * math.pi * r
arc_length = circumference / 5

# 중심각 구하기 (라디안)
central_angle_rad = arc_length / r
central_angle_deg = central_angle_rad * (180 / math.pi)

# 원주각 = 중심각 / 2
inscribed_angle = central_angle_deg / 2

# 검증
expected = 36.0
if abs(inscribed_angle - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')