from sympy import symbols, expand
x = symbols('x')
a, b = 3, 1
lhs = x**2 + a*x - 1
rhs = (x-1)*(x+b) + 3*x
rhs_expanded = expand(rhs)
if expand(lhs - rhs_expanded) == 0:
    print('VERIFY_PASS')
else:
    print('VERIFY_FAIL')