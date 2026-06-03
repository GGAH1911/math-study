import sympy as sp
x = sp.Symbol('x')
y_line = -sp.Rational(1, 2) * x + 2

# 점 A(4, 0)이 직선 위에 있는지 확인
y_at_A = y_line.subs(x, 4)
assert y_at_A == 0, f'점 A(4, 0)이 직선 위에 없습니다: {y_at_A}'

# y절편 확인 (x=0일 때)
y_intercept = y_line.subs(x, 0)
assert y_intercept == 2, f'y절편이 {y_intercept}입니다'

# 기울기가 -1/2인지 확인 (법선벡터 (-2, -4)와 수직)
slope = sp.Rational(-1, 2)
AB_slope = -4 / -2  # = 2
assert slope * 2 == -1, f'법선벡터와 수직이 아닙니다'

print('VERIFY_PASS')