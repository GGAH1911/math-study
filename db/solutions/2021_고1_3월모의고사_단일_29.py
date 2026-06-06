import sympy as sp
from sympy import symbols, expand, solve

a, b, c, x = symbols('a b c x', real=True)

# 주어진 함수: y = ax^2 + bx + c
f = a*x**2 + b*x + c

# 우리의 답: a=6, b=-12, c=7
a_val, b_val, c_val = 6, -12, 7

# 조건 1: 점 A(1,1)을 지남
check1 = a_val + b_val + c_val
print(f'조건 1 - 점 A 통과: {check1} == 1? {check1 == 1}')

# 조건 2: 꼭짓점이 (1, 1)임
vertex_x = -b_val / (2*a_val)
vertex_y = a_val*vertex_x**2 + b_val*vertex_x + c_val
print(f'꼭짓점: ({vertex_x}, {vertex_y}) == (1, 1)? {vertex_x == 1 and vertex_y == 1}')

# 조건 3: 삼각형 BDC의 넓이 = 12
# B = (0, c), C = (-b/a, c), D = (0, 1-a)
B = (0, c_val)
C = (-b_val/a_val, c_val)
D = (0, 1-a_val)

BD_length = abs(B[1] - D[1])
C_to_axis_dist = abs(C[0])
area = 0.5 * BD_length * C_to_axis_dist

print(f'B = {B}, C = {C}, D = {D}')
print(f'BD 길이 = {BD_length}')
print(f'C에서 y축까지 거리 = {C_to_axis_dist}')
print(f'삼각형 BDC 넓이 = {area} == 12? {area == 12}')

if check1 == 1 and vertex_x == 1 and vertex_y == 1 and area == 12:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')