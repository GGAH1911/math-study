import math

a = (math.sqrt(3) + 1) / 2

# 직선 y = x + 1 위의 점 P
x_p = a
y_p = x_p + 1

# P가 x > 0 조건 만족
assert x_p > 0

# OP가 나타내는 각 θ
theta = math.atan2(y_p, x_p)

# 동경 7θ
theta_7 = 7 * theta

# 두 동경이 일치하는지 확인 (0~2π 범위로 정규화)
def normalize_angle(angle):
    return angle % (2 * math.pi)

norm_theta = normalize_angle(theta)
norm_theta_7 = normalize_angle(theta_7)

# 오차 범위 내에서 같은지 확인
if abs(norm_theta - norm_theta_7) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')