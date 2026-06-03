from sympy import Matrix, Rational

# 정육면체 부피
cube_volume = 4**3

# 사면체 꼭짓점 (A가 원점)
A = [0, 0, 0]
B = [2, 0, 0]
C = [0, 2, 0]
D = [0, 0, 2]

# 사면체 부피: (1/6) * |det(B-A, C-A, D-A)|
matrix = Matrix([
    [B[0]-A[0], B[1]-A[1], B[2]-A[2]],
    [C[0]-A[0], C[1]-A[1], C[2]-A[2]],
    [D[0]-A[0], D[1]-A[1], D[2]-A[2]]
]).T

tetrahedron_volume = abs(matrix.det()) / 6

# 남은 부피
remaining_volume = cube_volume - tetrahedron_volume

# 정답 검증
answer = Rational(188, 3)
if remaining_volume == answer:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')