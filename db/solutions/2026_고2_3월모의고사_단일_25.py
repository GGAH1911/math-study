import sympy as sp
x, a = sp.symbols('x a', real=True)

# 원의 접선: x + y = 2, 즉 y = 2 - x
# 곡선: y = x^2 + ax + 2a
# 접선이 곡선에 접하므로: 2 - x = x^2 + ax + 2a
# 정리: x^2 + (a+1)x + (2a-2) = 0

eq = x**2 + (a+1)*x + (2*a - 2)
discriminant = sp.discriminant(eq, x)
print(f'Discriminant: {discriminant}')

# 판별식 = 0일 때
a_val = sp.solve(discriminant, a)
print(f'a values: {a_val}')

# a = 3일 때 검증
a_test = 3
curve = x**2 + a_test*x + 2*a_test  # y = x^2 + 3x + 6
line = 2 - x  # y = 2 - x

# 교점 구하기
intersection_eq = sp.Eq(curve, line)
intersection_points = sp.solve(intersection_eq, x)
print(f'Intersection x-values: {intersection_points}')

# x = -2에서 중근이므로
x_touch = intersection_points[0] if len(intersection_points) == 1 else -2
y_touch = 2 - x_touch

# 곡선에 대입
y_curve = x_touch**2 + a_test*x_touch + 2*a_test
print(f'Curve at x={x_touch}: y={y_curve}')
print(f'Line at x={x_touch}: y={y_touch}')

# 기울기 확인
curve_deriv = sp.diff(x**2 + a_test*x + 2*a_test, x)
slope_curve = curve_deriv.subs(x, x_touch)
slope_line = -1
print(f'Curve slope at x={x_touch}: {slope_curve}')
print(f'Line slope: {slope_line}')

if y_curve == y_touch and slope_curve == slope_line:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')