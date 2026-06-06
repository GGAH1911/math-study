import sympy as sp

x = sp.Symbol('x')

# 원래 직선 AB의 방정식: A(3, -1), B(4, -5)
# 기울기 = -4
line_AB = -4*x + 11

# 직선을 x축 방향 3, y축 방향 1만큼 평행이동
# (x, y) -> (x+3, y+1)이므로
# 새 직선 위의 점 (x, y)는 구 직선의 점 (x-3, y-1)을 만족
y = sp.Symbol('y')
new_line = -4*(x-3) + 11 + 1  # y의 값
new_line_simplified = -4*x + 24

# y절편 검증: x=0일 때
y_intercept = new_line_simplified.subs(x, 0)
if y_intercept == 24:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')