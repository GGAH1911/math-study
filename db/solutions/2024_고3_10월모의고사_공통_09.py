import math

a = 3/8

# 점 A
A_x = 4
A_y = math.log(a, 3)

# 점 B
B_x = math.log(2 * math.sqrt(2), 2)
B_y = math.log(3/2, 3)

# 선분 AB를 3:1로 외분하는 점 P
P_x = (3 * B_x - 1 * A_x) / (3 - 1)
P_y = (3 * B_y - 1 * A_y) / (3 - 1)

# P가 직선 y = 4x 위에 있는지 확인
y_expected = 4 * P_x

if abs(P_y - y_expected) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')