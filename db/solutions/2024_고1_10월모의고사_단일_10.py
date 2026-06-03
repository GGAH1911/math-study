import math

# 원의 반지름과 넓이 검증
k = 15
r_from_distance = k / math.sqrt(5)
area = math.pi * r_from_distance**2

# 원점에서 직선 2x + y - k = 0까지의 거리
dist = abs(-k) / math.sqrt(2**2 + 1**2)

# 원의 반지름과 거리가 같으면 접함
if abs(r_from_distance - dist) < 1e-10 and abs(area - 45*math.pi) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')