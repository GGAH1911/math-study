import sympy as sp
x, y = sp.symbols('x y')
# 포물선 y^2 = 4x 위의 점 (9, 6)
parabola_check = 6**2 - 4*9
assert parabola_check == 0, 'Point not on parabola'
# 포물선 위의 점 (9, 6)에서의 접선: y*y0 = 2(x + x0)
# 6y = 2(x + 9) => x = 3y - 9
# 준선 x = -1과의 교점
y_val = sp.Rational(8, 3)
x_val = -1
# 접선 방정식에 대입하여 검증
line_check = 6 * y_val - 2 * (x_val + 9)
assert line_check == 0, f'Point not on tangent line: {line_check}'
a_plus_b = x_val + y_val
assert a_plus_b == sp.Rational(5, 3), f'Sum mismatch: {a_plus_b}'
print('VERIFY_PASS')