import math

# 두 점의 좌표
x1, y1 = 1, 0
x2, y2 = 2, -3

# 두 점 사이의 거리
distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# 답: sqrt(10)
expected = math.sqrt(10)

if abs(distance - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')