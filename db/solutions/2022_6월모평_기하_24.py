import sympy as sp

x, y = sp.symbols('x y')

# 원래 타원 방정식
ellipse = x**2/8 + y**2/4 - 1

# 점 검증
point = (2, sp.sqrt(2))
assert ellipse.subs([(x, point[0]), (y, point[1])]) == 0, 'Point not on ellipse'

# 접선: x/4 + sqrt(2)*y/4 = 1  =>  x + sqrt(2)*y = 4
tangent = x + sp.sqrt(2)*y - 4

# 접선이 점을 지나는지
val_at_point = tangent.subs([(x, point[0]), (y, point[1])])
assert sp.simplify(val_at_point) == 0, 'Tangent does not pass through point'

# x절편 (y=0)
x_intercept = sp.solve(tangent.subs(y, 0), x)[0]
assert x_intercept == 4, f'x-intercept is {x_intercept}, not 4'

# 접선이 타원과 접하는지 (중근) 확인
y_from_tangent = sp.solve(tangent, y)[0]  # y = (4-x)/sqrt(2)
substituted = ellipse.subs(y, y_from_tangent)
substituted_expanded = sp.expand(substituted * 8)  # 분모 제거
discriminant = sp.discriminant(substituted_expanded, x)
assert sp.simplify(discriminant) == 0, 'Not a tangent line'

print('VERIFY_PASS')
