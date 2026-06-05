from sympy import *
x = symbols('x')
y = x * exp(-2*x)
y1 = diff(y, x)
y2 = diff(y1, x)
# 변곡점
infl = solve(y2, x)
x_A = infl[0]  # x=1
y_A = y.subs(x, x_A)
# 접선 기울기
slope = y1.subs(x, x_A)
# B의 x좌표
x_B = x_A - y_A / slope
# 넓이
area = Rational(1,2) * x_B * y_A
expected = exp(-2)
if simplify(area - expected) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')