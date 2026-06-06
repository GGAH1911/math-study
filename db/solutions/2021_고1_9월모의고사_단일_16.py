from sympy import symbols, solve, simplify, diff
import numpy as np

# 정리: 직사각형의 넓이 함수를 a의 함수로 표현
a = symbols('a', real=True, positive=True)

# 조건: 2a + 1 = -b + 4에서 b = 3 - 2a
b = 3 - 2*a
h = 2*a + 1

# 넓이
S = (b - a) * h
S_expanded = simplify(S)
print(f'Expanded S: {S_expanded}')

# 미분
dS_da = diff(S_expanded, a)
print(f'dS/da: {dS_da}')

# 극값
critical_points = solve(dS_da, a)
print(f'Critical points: {critical_points}')

# a = 1/4일 때 넓이 계산
a_opt = 1/4
b_opt = 3 - 2*a_opt
h_opt = 2*a_opt + 1
area = (b_opt - a_opt) * h_opt

print(f'When a = {a_opt}:')
print(f'  b = {b_opt}')
print(f'  h = {h_opt}')
print(f'  Area = {area}')
print(f'  Area as fraction = {area} = 27/8')

# 검증: 두 직선의 높이가 같은지 확인
left_height = 2*a_opt + 1
right_height = -b_opt + 4
print(f'\nVerification:')
print(f'  Left height (from l1): {left_height}')
print(f'  Right height (from l2): {right_height}')
print(f'  Heights equal: {abs(left_height - right_height) < 1e-10}')

# 최종 답 확인
if abs(area - 27/8) < 1e-10:
    print('\nVERIFY_PASS')
else:
    print('\nVERIFY_FAIL')