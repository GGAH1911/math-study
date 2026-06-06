from math import pi

# 주어진 조건
r = 8  # 반지름
theta = (3/4) * pi  # 중심각 (라디안)

# 부채꼴의 넓이 공식
area = (1/2) * r**2 * theta

# area = a * pi 형태로 표현
a = area / pi

# 정답 검증
if abs(a - 24) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')