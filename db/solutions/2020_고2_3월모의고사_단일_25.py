CANDIDATE = 36

from sympy import symbols, solve, simplify

x, y, z = symbols('x y z', real=True)

# z=0인 경우로 검증
z_val = 0

# 조건들: x^2 + y^2 = 62, xy = 13
# (x-y)^2 = (x+y)^2 - 4xy = (x^2+y^2+2xy) - 4xy = x^2+y^2-2xy
# (x+y)^2 = x^2 + y^2 + 2xy = 62 + 26 = 88
# (x-y)^2 = x^2 + y^2 - 2xy = 62 - 26 = 36

x_sq_plus_y_sq = 62
xy_prod = 13

# (x-y-2*0)^2 = (x-y)^2 계산
x_minus_y_squared = x_sq_plus_y_sq - 2*xy_prod
result = x_minus_y_squared

if result == CANDIDATE:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')