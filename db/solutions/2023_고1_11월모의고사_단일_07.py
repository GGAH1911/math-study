from fractions import Fraction

# 주어진 점들
A = (5, 1)
B = (-1, 4)
a, b = 3, 2
C = (a, b)

# AB를 2:1로 내분하는 점
P_x = (2 * B[0] + 1 * A[0]) / 3
P_y = (2 * B[1] + 1 * A[1]) / 3
P = (P_x, P_y)

# AC를 2:1로 외분하는 점
Q_x = (2 * C[0] - 1 * A[0]) / 1
Q_y = (2 * C[1] - 1 * A[1]) / 1
Q = (Q_x, Q_y)

# 두 점이 같은지 확인
if abs(P[0] - Q[0]) < 1e-9 and abs(P[1] - Q[1]) < 1e-9:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')