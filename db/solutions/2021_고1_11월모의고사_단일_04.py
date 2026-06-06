from sympy import symbols, solve, Eq
x, y = symbols('x y')
# 직선: y = 2x + 3
# 점 (3, 9)를 지나는가?
y_at_x3 = 2*3 + 3
assert y_at_x3 == 9, f'점 (3,9) 검증 실패: y={y_at_x3}'
# y절편 (x=0일 때)
y_intercept = 2*0 + 3
assert y_intercept == 3, f'y절편 검증 실패: {y_intercept}'
print('VERIFY_PASS')