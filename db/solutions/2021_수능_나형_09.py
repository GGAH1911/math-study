import sympy as sp
x = sp.Symbol('x')
# 원래 곡선
y_curve = x**3 - 3*x**2 + 2*x + 2
# 점 A에서의 기울기
derivative = sp.diff(y_curve, x)
slope_tangent = derivative.subs(x, 0)
print(f'접선의 기울기: {slope_tangent}')
# 수직선의 기울기
slope_perp = -1 / slope_tangent
print(f'수직선의 기울기: {slope_perp}')
# 점 A(0,2)를 지나는 수직선: y - 2 = slope_perp * (x - 0)
# y = slope_perp * x + 2
# x절편: y = 0일 때
x_intercept = -2 / slope_perp
print(f'x절편: {x_intercept}')
if x_intercept == 4:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')