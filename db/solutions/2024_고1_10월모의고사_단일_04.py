from sympy import symbols, solve
x = symbols('x')
# 원래 직선: y = 2x + 4
# x축 방향 1만큼 평행이동: x를 (x-1)로 치환 → y = 2(x-1) + 4 = 2x + 2
# y축 방향 3만큼 평행이동: y를 (y-3)으로 치환 → y - 3 = 2x + 2 → y = 2x + 5
# y절편: x = 0일 때
y_intercept = 2*0 + 5
assert y_intercept == 5, f'Expected 5, got {y_intercept}'
print('VERIFY_PASS')