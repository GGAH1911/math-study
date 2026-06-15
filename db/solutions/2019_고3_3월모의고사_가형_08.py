from sympy import symbols, diff, solve, Rational

x = symbols('x')
f = 1 / (x - 1)

# 점 (3/2, 2)가 곡선 위에 있는지 확인
point_x = Rational(3, 2)
point_y = f.subs(x, point_x)
assert point_y == 2, f"Point not on curve: {point_y} != 2"

# 접선의 기울기
f_prime = diff(f, x)
slope = f_prime.subs(x, point_x)
assert slope == -4, f"Slope incorrect: {slope} != -4"

# 접선 방정식: y - 2 = -4(x - 3/2)
# y = -4x + 8

# y축과의 교점 (x=0): y = 8
y_intercept = 8

# x축과의 교점 (y=0): 0 = -4x + 8, x = 2
x_intercept = 2

# 직각삼각형의 넓이
area = (x_intercept * y_intercept) / 2
assert area == 8, f"Area incorrect: {area} != 8"

print('VERIFY_PASS')