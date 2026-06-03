import math
from sympy import symbols, solve, sqrt, simplify

# 원의 중심
center_x, center_y = 2, 3

# 반지름
r = math.sqrt(10)

# 직선 y = x + 5를 원의 방정식에 대입
x = symbols('x', real=True)
y_expr = x + 5

# (x-2)^2 + (y-3)^2 = r^2
# (x-2)^2 + (x+5-3)^2 = 10
# (x-2)^2 + (x+2)^2 = 10
eq = (x - 2)**2 + (x + 2)**2 - 10
solutions = solve(eq, x)

# 두 교점
A_x, B_x = solutions[0], solutions[1]
A_y = A_x + 5
B_y = B_x + 5

# 현의 길이 확인
dist_AB = math.sqrt((A_x - B_x)**2 + (A_y - B_y)**2)
print(f'AB length: {dist_AB}, expected: {2*math.sqrt(2)}')

# 두 점이 원 위에 있는지 확인
check_A = (A_x - 2)**2 + (A_y - 3)**2
check_B = (B_x - 2)**2 + (B_y - 3)**2
print(f'A on circle: {abs(check_A - 10) < 1e-10}')
print(f'B on circle: {abs(check_B - 10) < 1e-10}')

if abs(dist_AB - 2*math.sqrt(2)) < 1e-9 and abs(check_A - 10) < 1e-10 and abs(check_B - 10) < 1e-10:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')