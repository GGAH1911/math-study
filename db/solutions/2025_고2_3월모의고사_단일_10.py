import math

# 주어진 조건: 사각형 ACDB의 넓이 = 18
# 답: AB = 2√10

k = 2

# 점 A, B 좌표
A_x, A_y = k, math.sqrt(2*k)
B_x, B_y = 4*k, math.sqrt(2*4*k)
C_x, C_y = k, 0
D_x, D_y = 4*k, 0

# 사다리꼴 ACDB의 넓이 (AC와 BD가 수직)
AC_length = A_y
BD_length = B_y
CD_length = D_x - C_x

area = 0.5 * (AC_length + BD_length) * CD_length

# AB의 길이
AB = math.sqrt((B_x - A_x)**2 + (B_y - A_y)**2)

# 검증
if abs(area - 18) < 1e-9 and abs(AB - 2*math.sqrt(10)) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')