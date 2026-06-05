import sympy as sp
x = sp.Symbol('x')
a_val = 6
f = sp.Abs(x + 3)
g = 2*x + a_val
product = f * g

# x = -3 근처에서 미분가능성 확인
# 우측 미분계수
right_expr = (x + 3) * (2*x + a_val)
right_deriv = sp.diff(right_expr, x)
right_deriv_at_minus3 = right_deriv.subs(x, -3)

# 좌측 미분계수  
left_expr = -(x + 3) * (2*x + a_val)
left_deriv = sp.diff(left_expr, x)
left_deriv_at_minus3 = left_deriv.subs(x, -3)

if right_deriv_at_minus3 == left_deriv_at_minus3:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')