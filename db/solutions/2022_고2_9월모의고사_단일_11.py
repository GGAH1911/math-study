import numpy as np

# 점 A와 B의 좌표
A_x, A_y = 4, 1
B_x, B_y = 3, -1

# 검증 1: A가 y=log_4(x)에서 y=1을 만족
assert abs(A_y - np.log(A_x) / np.log(4)) < 1e-9

# 검증 2: B가 y=-log_4(x+1)을 만족
y_B_expected = -np.log(B_x + 1) / np.log(4)
assert abs(B_y - y_B_expected) < 1e-9

# 검증 3: x축이 삼각형 OAB의 넓이를 이등분
# 직선 AB: y = 2x - 7, x축과의 교점 C_x = 3.5
C_x = 3.5
area_OAC = 0.5 * abs(A_x * 0 - C_x * A_y)
area_OCB = 0.5 * abs(C_x * B_y - B_x * 0)
assert abs(area_OAC - area_OCB) < 1e-9

# 답: OB의 길이
OB_length = np.sqrt(B_x**2 + B_y**2)
assert abs(OB_length - np.sqrt(10)) < 1e-9

print('VERIFY_PASS')