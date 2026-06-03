from sympy import *

a_val = Rational(6, 5)
b_val = Rational(8, 5)
x, y = symbols('x y')

# P가 x^2+y^2=4, x>=0 위에 있는지 확인
assert a_val**2 + b_val**2 == 4, 'P not on circle'
assert a_val >= 0, 'a < 0'

# 직선 a*x + b*y = 2와 원 (x+5)^2+y^2=16의 교점
line_eq = a_val*x + b_val*y - 2
circle_eq = (x+5)**2 + y**2 - 16
sols = solve([line_eq, circle_eq], [x, y])

# y >= 0인 교점만 선택
valid = [(sx, sy) for sx, sy in sols if sy >= 0]

# 유일해인지 확인
if len(valid) != 1:
    print('VERIFY_FAIL')
else:
    Qx, Qy = valid[0]
    dot = a_val*Qx + b_val*Qy
    if dot == 2:
        print('a+b =', a_val + b_val)
        print('VERIFY_PASS')
    else:
        print('VERIFY_FAIL')
