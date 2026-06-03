import math

theta = math.atan(2) + math.pi  # 3사분면 각 (tan=2, pi < theta < 3pi/2)

# 조건 확인
assert math.pi < theta < 1.5 * math.pi, 'quadrant check failed'

# tan theta = 2 확인
assert abs(math.tan(theta) - 2) < 1e-9, 'tan check failed'

# cos theta 값 확인
result = math.cos(theta)
expected = -math.sqrt(5) / 5

if abs(result - expected) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
