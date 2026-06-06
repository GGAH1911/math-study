from sympy import symbols, diff, simplify

# 원래 곡선
x = symbols('x')
y = x**3 - 5*x**2 + 3*x + 6

# 점 (1, 5) 확인
y_at_1 = y.subs(x, 1)
assert y_at_1 == 5, f'점이 곡선 위에 없음: y(1)={y_at_1}'

# 접선의 기울기
dy_dx = diff(y, x)
slope = dy_dx.subs(x, 1)
assert slope == -4, f'기울기 계산 오류: {slope}'

# 접선의 방정식: y - 5 = slope * (x - 1)
# y = slope * x + (5 - slope * 1)
y_intercept = 5 - slope * 1
assert y_intercept == 9, f'y절편 계산 오류: {y_intercept}'

print('VERIFY_PASS')