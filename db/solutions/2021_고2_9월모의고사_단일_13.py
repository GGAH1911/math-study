import math

# 주어진 조건에서 구한 theta
theta = 2 * math.pi / 7

# 부채꼴의 반지름
r = 2

# 부채꼴 넓이
area = 0.5 * r**2 * theta
expected_area = 4 * math.pi / 7

# 검증: 동경 일치 조건 확인
# 8*theta와 theta의 동경이 일치하는지 확인
difference = 8 * theta - theta
expected_diff = 2 * math.pi  # 2πk where k=1

# 검증
if abs(area - expected_area) < 1e-10 and abs(difference - expected_diff) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')