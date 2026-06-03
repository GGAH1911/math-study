import sympy as sp

# 구한 값
a, b, c = 4, -6, 10

# A, B 좌표
A = (a, b, -5)
B = (-8, 6, c)

# 조건 1: AB의 중점이 zx평면 위 (y=0)
midpoint_y = (A[1] + B[1]) / 2
check1 = (midpoint_y == 0)

# 조건 2: AB를 1:2로 내분하는 점이 y축 위
# 내분점 = (2A + 1B)/3
P_x = (2*A[0] + B[0]) / 3
P_y = (2*A[1] + B[1]) / 3
P_z = (2*A[2] + B[2]) / 3

check2 = (P_x == 0 and P_z == 0)

# 답 검증
result = a + b + c

if check1 and check2 and result == 8:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')