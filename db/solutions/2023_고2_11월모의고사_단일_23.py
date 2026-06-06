import math

# 문제의 주어진 조건
central_angle = (4 * math.pi) / 5  # 중심각 (라디안)
arc_length = 12 * math.pi  # 호의 길이

# 구한 답
r = 15

# 검증: 호의 길이 = r × θ
calculated_arc = r * central_angle

if abs(calculated_arc - arc_length) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')