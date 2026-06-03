import sympy as sp
x = sp.Symbol('x')

# 원래 문제: x(x+1) + 2(x+1) = x^2 + ax + b (항등식)
left_side = x*(x+1) + 2*(x+1)
right_side = x**2 + 3*x + 2

# 좌변과 우변 전개
left_expanded = sp.expand(left_side)
right_expanded = sp.expand(right_side)

# 항등식인지 확인
if left_expanded == right_expanded:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')