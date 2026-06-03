from sympy import symbols, solve, expand

# 주어진 조건
# x + y - z = 5
# xy - yz - zx = 4

# 첫 번째 조건에서: x + y = z + 5
# 두 번째 조건에서: xy - z(x+y) = 4
# 따라서: xy = z^2 + 5z + 4

z = symbols('z', real=True)

# x, y는 t^2 - (x+y)t + xy = 0의 해
# t^2 - (z+5)t + (z^2+5z+4) = 0

# x^2 + y^2 = (x+y)^2 - 2xy
sum_xy = z + 5
prod_xy = z**2 + 5*z + 4

x_squared_plus_y_squared = sum_xy**2 - 2*prod_xy
x_squared_plus_y_squared = expand(x_squared_plus_y_squared)
# = (z+5)^2 - 2(z^2+5z+4)
# = z^2 + 10z + 25 - 2z^2 - 10z - 8
# = -z^2 + 17

result = x_squared_plus_y_squared + z**2
result = expand(result)
# = (-z^2 + 17) + z^2 = 17

if result == 17:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')