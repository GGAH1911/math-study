import sympy as sp

a = sp.Symbol('a', real=True, positive=True)

# |OP|^2
OP_squared = a**2 + a**8

# H의 좌표
x_H = (a + 2*a**4 - 2) / 5
y_H = (4*a**4 + 2*a + 1) / 5

# |OH|^2
OH_squared = x_H**2 + y_H**2

# 비율
ratio = OP_squared / OH_squared

# 극한
limit_value = sp.limit(ratio, a, sp.oo)

if limit_value == sp.Rational(5, 4):
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')