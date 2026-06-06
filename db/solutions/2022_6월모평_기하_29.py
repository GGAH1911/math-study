import math

# 점들의 좌표 정의
sqrt5 = math.sqrt(5)
A = (3 + sqrt5, 2 + 2*sqrt5)
B = (3 + 3*sqrt5, 2 + 6*sqrt5)
C = (-2, 2 + 2*sqrt5)
D = (-2, 2 + 6*sqrt5)

# 점 A가 포물선 y² = 8x 위에 있는지 확인
y_sq_A = A[1]**2
_8x_A = 8*A[0]
assert abs(y_sq_A - _8x_A) < 1e-9, f'A not on parabola y²=8x: {y_sq_A} vs {_8x_A}'

# 점 A가 직선 y = 2x - 4 위에 있는지 확인
y_line_A = 2*A[0] - 4
assert abs(A[1] - y_line_A) < 1e-9, f'A not on line y=2x-4'

# a = 2√5에 대해 A가 포물선 (y-2a)² = 8(x-a) 위에 있는지 확인
a = 2*sqrt5
LHS = (A[1] - 2*a)**2
RHS = 8*(A[0] - a)
assert abs(LHS - RHS) < 1e-9, f'A not on parabola (y-2a)²=8(x-a): {LHS} vs {RHS}'

# 점 B가 직선 y = 2x - 4 위에 있는지 확인
y_line_B = 2*B[0] - 4
assert abs(B[1] - y_line_B) < 1e-9, f'B not on line y=2x-4'

# 점 B가 포물선 (y-2a)² = 8(x-a) 위에 있는지 확인
LHS_B = (B[1] - 2*a)**2
RHS_B = 8*(B[0] - a)
assert abs(LHS_B - RHS_B) < 1e-9, f'B not on parabola: {LHS_B} vs {RHS_B}'

# 거리 계산
AC = abs(A[0] - C[0])
BD = abs(B[0] - D[0])
AB = math.sqrt((B[0] - A[0])**2 + (B[1] - A[1])**2)

# k 계산
k = AC + BD - AB
k_squared = k**2

# 80에 수렴하는지 확인
assert abs(k_squared - 80) < 1e-9, f'k² = {k_squared} is not 80'
print('VERIFY_PASS')