import math

p = math.log2(5)

# 점들의 좌표
A_x, A_y = p, 2**p + 1
B_x, B_y = p, 0
C_x, C_y = p + 2, 1

# 삼각형 ABC의 넓이 (신발끈 공식)
area = 0.5 * abs((A_x * (B_y - C_y) + B_x * (C_y - A_y) + C_x * (A_y - B_y)))

# 조건 검증
if abs(area - 6.0) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')