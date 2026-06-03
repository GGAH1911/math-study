from sympy import symbols, expand, Eq, solve
x, a, b = symbols('x a b')
lhs = x**2 + (a+2)*x
rhs = x**2 + 4*x + (b-1)
a_val, b_val = 2, 1
lhs_sub = lhs.subs([(a, a_val), (b, b_val)])
rhs_sub = rhs.subs([(a, a_val), (b, b_val)])
if expand(lhs_sub - rhs_sub) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')