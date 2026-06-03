import math
from sympy import sqrt, symbols, simplify, solve

# 구한 답
a = 27/4
x1 = 27/20
x2 = 15/4

# 점 A, B, C의 좌표
A = (x1, a/x1)
B = (x2, a/x2)
C = (x1, 0)

print(f'A = {A}')
print(f'B = {B}')
print(f'C = {C}')

# 조건 1: AB = 4
AB = math.sqrt((B[0]-A[0])**2 + (B[1]-A[1])**2)
print(f'AB = {AB}, 조건: AB = 4')
assert abs(AB - 4) < 1e-10, f'AB condition failed: {AB}'

# 조건 2: BC = 3
BC = math.sqrt((C[0]-B[0])**2 + (C[1]-B[1])**2)
print(f'BC = {BC}, 조건: BC = 3')
assert abs(BC - 3) < 1e-10, f'BC condition failed: {BC}'

# 조건 3: 각 ABC = 90도 (벡터의 내적이 0)
BA = (A[0]-B[0], A[1]-B[1])
BC_vec = (C[0]-B[0], C[1]-B[1])
dot_product = BA[0]*BC_vec[0] + BA[1]*BC_vec[1]
print(f'BA · BC = {dot_product}, 조건: 내적 = 0')
assert abs(dot_product) < 1e-10, f'Perpendicularity condition failed: {dot_product}'

# 조건 4: A, B는 y = a/x 위에 있음
check_A = abs(A[1] - a/A[0])
check_B = abs(B[1] - a/B[0])
print(f'A가 곡선 위에 있는지: {check_A < 1e-10}')
print(f'B가 곡선 위에 있는지: {check_B < 1e-10}')
assert check_A < 1e-10 and check_B < 1e-10

print('VERIFY_PASS')