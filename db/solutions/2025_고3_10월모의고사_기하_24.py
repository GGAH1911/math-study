import sympy as sp

# 원래 포물선 y^2 = 4x
x, y = sp.symbols('x y', real=True)
parabola = y**2 - 4*x

# 점 (4, 4)에서의 접선의 기울기 = 1/2
# 접선: y - 4 = (1/2)(x - 4) => y = (1/2)x + 2
tangent_slope = sp.Rational(1, 2)
tangent_eq = y - sp.Rational(1, 2)*x - 2

# 접선이 포물선과 점 (4, 4)에서 접하는지 확인
# 포물선에 접선 방정식을 대입
tangent_y = sp.Rational(1, 2)*x + 2
substituted = parabola.subs(y, tangent_y)
substituted_simplified = sp.expand(substituted)

# x = 4에서의 중근 확인
roots = sp.solve(substituted_simplified, x)

if roots == [4]:
    # 접점이 (4, 4)인지 확인
    y_at_4 = tangent_y.subs(x, 4)
    if y_at_4 == 4:
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
else:
    print('VERIFY_FAIL')