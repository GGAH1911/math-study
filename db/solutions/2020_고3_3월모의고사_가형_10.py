from sympy import symbols, integrate, solve, diff, Rational
x = symbols('x')
a = Rational(1, 2)
# 포물선과 직선이 x=2에서 접하는지 확인
parabola = a*x**2 + 2
line_pos = 2*x
# x=2에서 교점
assert parabola.subs(x, 2) == line_pos.subs(x, 2) == 4
# 도함수가 같은지 확인
assert diff(parabola, x).subs(x, 2) == diff(line_pos, x) == 2
# 음영 영역 넓이: x in [0,2]에서
area_half = integrate(parabola - line_pos, (x, 0, 2))
total_area = 2 * area_half
assert total_area == Rational(8, 3)
print('VERIFY_PASS')