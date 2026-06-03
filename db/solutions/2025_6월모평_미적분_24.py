from sympy import *
x_val = Integer(1)
y_val = pi/2
# 곡선 위의 점 검증
curve_check = x_val*sin(2*y_val) + 3*x_val
# 음함수 미분: dy/dx = -(sin2y + 3) / (2x*cos2y)
sin2y = sin(2*y_val)
cos2y = cos(2*y_val)
dydx = (-sin2y - 3) / (2*x_val*cos2y)
dydx_val = simplify(dydx)
if simplify(curve_check - 3) == 0 and simplify(dydx_val - Rational(3,2)) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')
    print('curve_check:', curve_check, 'dydx:', dydx_val)
