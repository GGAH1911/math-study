import sympy as sp
from sympy import symbols, solve, Abs

# a = -8
a = -8
x = symbols('x', real=True)

# 교점 확인
line1 = -x/2  # y = -x/2
hyperbola = a/x  # y = a/x

# 교점 계산
intersection_eq = line1 - hyperbola
roots = solve(intersection_eq, x)
print(f'교점의 x좌표: {roots}')

# a = -8일 때 점의 좌표
x_A = 4
y_A = -2
x_B = -4
y_B = 2
x_C = -4
y_C = -2

# 두 함수 검증
print(f'점 A({x_A}, {y_A}): 정비례={-x_A/2}, 반비례={a/x_A}')
print(f'점 B({x_B}, {y_B}): 정비례={-x_B/2}, 반비례={a/x_B}')

# 삼각형 넓이 계산 (신발끈 공식)
area = 0.5 * abs((x_A*(y_B - y_C) + x_B*(y_C - y_A) + x_C*(y_A - y_B)))
print(f'삼각형 ABC 넓이: {area}')

if area == 16:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')