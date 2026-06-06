import math

# 삼각형의 변의 길이
AB, BC, CA = 25, 17, 26

# 좌표계: H를 원점으로 설정
H = (0, 0)
B = (-7, 0)
C = (10, 0)
A = (0, 24)

# 조건 검증
# AC = 26
AC_dist = math.sqrt((C[0] - A[0])**2 + (C[1] - A[1])**2)
assert abs(AC_dist - 26) < 1e-10, f'AC = {AC_dist}'

# BC = 17
BC_dist = math.sqrt((C[0] - B[0])**2 + (C[1] - B[1])**2)
assert abs(BC_dist - 17) < 1e-10, f'BC = {BC_dist}'

# 넓이 = 204
area = 0.5 * abs((B[0] - A[0]) * (C[1] - A[1]) - (C[0] - A[0]) * (B[1] - A[1]))
assert abs(area - 204) < 1e-10, f'Area = {area}'

# H는 A에서 BC로 내린 수선의 발
# BC는 y=0 직선이므로, H는 A의 x좌표와 같아야 함
assert H[0] == A[0], 'H is not the foot of perpendicular'
assert H[1] == 0, 'H is not on BC'

# 내심의 좌표
a, b, c = BC, CA, AB  # a = BC, b = CA, c = AB
perimeter = a + b + c
I_x = (a * A[0] + b * B[0] + c * C[0]) / perimeter
I_y = (a * A[1] + b * B[1] + c * C[1]) / perimeter
I = (I_x, I_y)

# IH^2 계산
IH_squared = (I[0] - H[0])**2 + (I[1] - H[1])**2

assert abs(IH_squared - 37) < 1e-10, f'IH^2 = {IH_squared}'
print('VERIFY_PASS')