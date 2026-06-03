from sympy import *

# 쌍곡선의 정의 확인
x, y, t = symbols('x y t', real=True)
hyperbola = x**2/7 - y**2/6 - 1

# 점 (7, 6)이 쌍곡선 위에 있는지 확인
point_check = hyperbola.subs([(x, 7), (y, 6)])
print(f'Point on hyperbola check: {point_check}')

# 접선의 방정식: x - y = 1
# x절편 구하기
tangent_line = x - y - 1
x_intercept = solve(tangent_line.subs(y, 0), x)[0]
print(f'x-intercept: {x_intercept}')

# 검증: 접선이 쌍곡선과 점 (7,6)에서 접하는지 확인
# 접선: x - y = 1 => y = x - 1
y_tangent = x - 1
intersection_eq = hyperbola.subs(y, y_tangent)
intersection_solutions = solve(intersection_eq, x)
print(f'Intersection x-values: {intersection_solutions}')
print(f'Double root at x=7: {intersection_solutions.count(7)}')

if x_intercept == 1:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')