import math

# 타원 방정식: x^2/17 + y^2/8 = 1
a_squared = 17
b_squared = 8

# 초점까지의 거리
c_squared = a_squared - b_squared
c = math.sqrt(c_squared)

# 두 초점 사이의 거리
focal_distance = 2 * c

# 검증
if abs(focal_distance - 6) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')