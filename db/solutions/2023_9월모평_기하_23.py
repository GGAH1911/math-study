# 주어진 조건: A(a, 1, -1), B(-5, b, 3), 중점(8, 3, 1)
a = 21
b = 5

# 선분 AB의 중점 계산
midpoint_x = (a + (-5)) / 2
midpoint_y = (1 + b) / 2
midpoint_z = ((-1) + 3) / 2

# 검증
if midpoint_x == 8 and midpoint_y == 3 and midpoint_z == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')