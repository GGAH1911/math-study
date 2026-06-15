from sympy import symbols, Rational

# 세 점의 좌표
A = (2, 6, -3)
B = (-5, 7, 4)
C = (3, -1, 5)

# 무게중심 계산
G_x = (A[0] + B[0] + C[0]) / 3
G_y = (A[1] + B[1] + C[1]) / 3
G_z = (A[2] + B[2] + C[2]) / 3

a = G_y
b = G_z

# 검증: G의 x 좌표가 0인지 확인
assert G_x == 0, f'x좌표 오류: {G_x}'

# 답 확인
answer = a + b
assert answer == 6, f'계산 오류: a={a}, b={b}, a+b={answer}'

print('VERIFY_PASS')