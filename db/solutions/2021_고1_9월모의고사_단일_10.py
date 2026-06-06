import sympy as sp
x, y = sp.symbols('x y')
# 원의 방정식: x^2 + y^2 = 10
circle_eq = x**2 + y**2 - 10
# 점 (3, 1)이 원 위에 있는지 확인
point_check = circle_eq.subs([(x, 3), (y, 1)])
assert point_check == 0, 'Point not on circle'
# 접선의 방정식: y = -3x + 10
# 접선이 점 (3, 1)을 지나는지 확인
line_eq = -3 * 3 + 10
assert line_eq == 1, 'Line does not pass through point'
# 접선과 원이 (3, 1)에서만 만나는지 확인 (한 점에서만 접함)
line_y = -3*x + 10
sub_circle = circle_eq.subs(y, line_y)
solutions = sp.solve(sub_circle, x)
assert len(solutions) == 1 and solutions[0] == 3, 'Not tangent line'
print('VERIFY_PASS')