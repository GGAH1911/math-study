from sympy import symbols, simplify
x, y = symbols('x y')
# 쌍곡선: x^2/2 - y^2/7 = 1
hyperbola = x**2/2 - y**2/7 - 1
# 점 (4, 7)에서의 접선 (미분을 이용하면): 4x/2 - 7y/7 = 1 ⟹ 2x - y = 1
tangent_line = 2*x - y - 1
# y=0일 때 x값
x_intercept = 1/2
# 검증: 접선이 점 (4,7)을 지나는가?
y_at_point = 2*4 - 1
if y_at_point == 7 and 2*x_intercept - 0 - 1 == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')