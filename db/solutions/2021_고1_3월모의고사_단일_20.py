from sympy import sqrt, simplify

sqrt3 = sqrt(3)

# D의 좌표
d_x = 2 - sqrt3/3
e_x = 2 + sqrt3/3

# 점 정의
A = (0, 0)
B = (3, 0)
C = (0, 3)
D = (d_x, 0)
E = (e_x, 0)
F = (2, 1)

# 정삼각형 조건 확인
DE_squared = (e_x - d_x)**2
EF_squared = (2 - e_x)**2 + 1
FD_squared = (2 - d_x)**2 + 1

s_squared = simplify((2*sqrt3/3)**2)

DE_check = simplify(DE_squared - s_squared) == 0
EF_check = simplify(EF_squared - s_squared) == 0
FD_check = simplify(FD_squared - s_squared) == 0

# 벡터 계산
CA = (A[0] - C[0], A[1] - C[1])
CD = (D[0] - C[0], D[1] - C[1])

# tan(∠DCA) = |cross| / dot
dot_product = CA[0]*CD[0] + CA[1]*CD[1]
cross_product = CA[0]*CD[1] - CA[1]*CD[0]

tan_angle = simplify(abs(cross_product) / dot_product)
answer = (6 - sqrt3) / 9

if simplify(tan_angle - answer) == 0 and DE_check and EF_check and FD_check:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')