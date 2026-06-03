import sympy as sp
x, a = sp.symbols('x a')

# 원래 곡선
y_curve = x**3 - 5*x**2 + 6*x

# 점 (3, 0)이 곡선 위에 있는지 확인
y_at_3 = y_curve.subs(x, 3)
assert y_at_3 == 0, f'Point (3, 0) not on curve: {y_at_3}'

# 도함수
y_prime = sp.diff(y_curve, x)

# x=3에서의 기울기
slope = y_prime.subs(x, 3)
assert slope == 3, f'Slope at x=3 is {slope}, expected 3'

# 접선 방정식: y - 0 = slope * (x - 3)
# y = 3(x - 3) = 3x - 9
tangent_line = slope * (x - 3)

# 접선이 (5, a)를 지나는지 확인
a_value = tangent_line.subs(x, 5)
assert a_value == 6, f'a should be 6, got {a_value}'

print('VERIFY_PASS')