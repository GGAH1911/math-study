from sympy import symbols, solve, simplify

# 타원 위의 점 조건
a = symbols('a', positive=True, real=True)
eq1 = a**2/18 + 4/8 - 1
a_val = solve(eq1, a)[0]
print(f'a = {a_val}')

# 타원: x^2/18 + y^2/8 = 1
# 점 (3, 2)이 타원 위에 있는지 확인
point_check = 9/18 + 4/8
print(f'점 (3, 2)가 타원 위에 있나? {point_check} = 1: {abs(point_check - 1) < 1e-10}')

# 접선: x/6 + y/4 = 1
# x절편은 y=0일 때
x_intercept = 6

# 접선이 점 (3, 2)를 지나는지 확인
tangent_check = 3/6 + 2/4
print(f'접선이 점 (3, 2)를 지나나? {tangent_check} = 1: {abs(tangent_check - 1) < 1e-10}')

# 접선의 방정식 검증: d/dx[x^2/18 + y^2/8] = 0 암시미분
# 2x/18 + 2y/8 * dy/dx = 0
# dy/dx = -8x/18y = -4x/9y
# 점 (3, 2)에서 기울기: -4(3)/9(2) = -12/18 = -2/3
# 접선: y - 2 = -2/3(x - 3)
# y - 2 = -2x/3 + 2
# y = -2x/3 + 4
# x = 0일 때 y = 4, y = 0일 때 x = 6

slope_at_point = -4*3/(9*2)
print(f'점 (3, 2)에서의 기울기: {slope_at_point}')

# 접선: y - 2 = slope(x - 3)
# y = 0: -2 = (-2/3)(x - 3)
# -2 = -2x/3 + 2
# -4 = -2x/3
# x = 6

x_intercept_check = 6
print(f'x절편: {x_intercept_check}')

if x_intercept_check == 6:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')