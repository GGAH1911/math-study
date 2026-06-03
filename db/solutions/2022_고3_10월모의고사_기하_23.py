# 주어진 조건: A(3, a, -2), B(-1, 3, a)
# 중점이 xy평면(z=0) 위에 있을 때 a의 값

a = 2

# 중점의 좌표
midpoint_x = (3 + (-1)) / 2
midpoint_y = (a + 3) / 2
midpoint_z = (-2 + a) / 2

# z좌표가 0인지 확인
if abs(midpoint_z) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')