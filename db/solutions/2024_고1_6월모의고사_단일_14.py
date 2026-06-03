import sympy as sp
from sympy import symbols, solve, sqrt

x, a = symbols('x a')

# 포물선 정의
parabola = -x**2 + 4*x + 5

# 포물선이 x축과 만나는 점
roots_parabola = solve(parabola, x)
print(f'x축과의 교점: {roots_parabola}')
B_x, C_x = sorted(roots_parabola)
B = (B_x, 0)
C = (C_x, 0)
print(f'B = {B}, C = {C}')

# 직선과 포물선의 접점 조건
line = 2*x + a
eq = parabola - line
discriminant = eq.as_poly(x).discriminant()
print(f'판별식: {discriminant}')

a_val = solve(discriminant, a)[0]
print(f'a = {a_val}')

# 점 A 구하기
eq_A = parabola - (2*x + a_val)
A_x = solve(eq_A, x)[0]
A_y = parabola.subs(x, A_x)
A = (A_x, A_y)
print(f'A = {A}')

# 삼각형의 넓이 계산
BC_length = abs(C_x - B_x)
height = abs(A_y)
area = sp.Rational(1, 2) * BC_length * height
print(f'BC 길이: {BC_length}, 높이: {height}')
print(f'삼각형 ABC의 넓이: {area}')

if area == 24:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')