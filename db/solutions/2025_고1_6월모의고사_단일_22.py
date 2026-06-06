from sympy import symbols, expand, Eq, solve
x, a, b = symbols('x a b')
# 좌변
lhs = x**2 + (a+1)*x + 8
# 우변
rhs = x**2 + 10*x + b
# 조건: a=9, b=8일 때 항등식 확인
a_val, b_val = 9, 8
lhs_sub = lhs.subs([(a, a_val), (b, b_val)])
rhs_sub = rhs.subs([(a, a_val), (b, b_val)])
# 다항식이 같은지 확인
if expand(lhs_sub - rhs_sub) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')